import QuantumBlockEncoding.BlockEncoding
import QuantumBlockEncoding.CircuitSemantics

/-!
# Guseynov-Huang-Liu 2025 construction skeleton

This file turns the paper's main block-encoding construction into Lean data.
It does not yet prove matrix-level correctness; instead it fixes the statement
shape, resource formulas, and decomposition targets that future AI-generated
gate-level circuits must satisfy.
-/

namespace QuantumBlockEncoding
namespace GHL2025

open CostExpr

structure OneTermRobinParameters where
  n : Nat
  kappa : Nat
  functionPieces : Nat
  polynomialDegreeCost : Nat
deriving Repr, DecidableEq

/--
Classical specification of the indicator oracle U_indic(K1,K2).
Returns `true` when row index `i` is in the bulk region [K1, K2],
meaning U_indic maps |i⟩|0⟩ → |i⟩|1⟩.
Returns `false` for boundary rows (0 ≤ i < K1 or K2 < i),
meaning U_indic maps |i⟩|0⟩ → |i⟩|0⟩.
main.tex:1060-1065 --/
def isBulkRow (K1 K2 i : Nat) : Bool :=
  K1 ≤ i && i ≤ K2

/--
Complement of isBulkRow: returns true for boundary rows (j < K1 or K2 < j).
The paper's boundary set is {0,...,K1-1} union {K2+1,...,2^n-1}.
main.tex:1113, 1035-1038 --/
def isBoundaryRow (K1 K2 _gridSize : Nat) (j : Nat) : Bool :=
  j < K1 || K2 < j

/--
Detailed register partition matching the wavefunction ket labels
in Eq. ROBIN clarified (main.tex:1113-1117).
Each field is the qubit count for one register in the circuit.
Total signal qubits = m_f + 1 + ceil(log2 kappa) + 4 (indicator + ancilla + 1),
plus n system qubits. Pure ancillas appear in two groups totaling 2n.
figure:1_term_ROBIN caption --/
structure RobinRegisterPartition where
  /-- m_f = ceil(log2 n) + ceil(log2 G_f) + 3 qubits for function oracle O_f.
  main.tex:1141 --/
  mfQubits : Nat
  /-- 1 indicator ancilla qubit set by U_indic. main.tex:1060-1065, 1113 --/
  indicatorQubit : Nat
  /-- ceil(log2 kappa) qubits for sparse index s. main.tex:1113 --/
  sparseIndexQubits : Nat
  /-- n - ceil(log2 kappa) qubits used as pure ancillas for O_D^BS register.
  main.tex:1113, 1149 --/
  odPureAncillaQubits : Nat
  /-- n system qubits for row index j. main.tex:1113 --/
  systemQubits : Nat
  /-- 1 ancilla qubit (also pure ancilla after cleanup). main.tex:1113, 1159 --/
  ancillaQubit : Nat
deriving Repr, DecidableEq

/--
Total qubits used by the register partition (all registers summed).
-/
def RobinRegisterPartition.totalQubits (rp : RobinRegisterPartition) : Nat :=
  rp.mfQubits + rp.indicatorQubit + rp.sparseIndexQubits +
  rp.odPureAncillaQubits + rp.systemQubits + rp.ancillaQubit

/--
Default register partition from concrete parameters.
figure:1_term_ROBIN --/
def defaultRobinRegisterPartition (p : OneTermRobinParameters) : RobinRegisterPartition where
  mfQubits := clog2 p.n + clog2 p.functionPieces + 3
  indicatorQubit := 1
  sparseIndexQubits := clog2 p.kappa
  odPureAncillaQubits := p.n - clog2 p.kappa
  systemQubits := p.n
  ancillaQubit := 1

/--
Pure ancilla qubits visible in the Eq. ROBIN register partition:
`(n - ceil(log2 kappa)) + 1` from the O_D^BS register plus the trailing
ancilla.

This is intentionally narrower than the theorem's full `2n` pure-ancilla
budget.  The theorem-level count in `oneTermRobinLayout` and
`oneTermRobinResourceExpr` also includes internal workspace required by the
banded sparse-access and oracle subcircuits.  Keep this distinction explicit to
avoid treating the ket-level register partition as the full resource proof.
figure:1_term_ROBIN caption, main.tex:1149, main.tex:1131-1136
-/
def RobinRegisterPartition.totalPureAncillas (rp : RobinRegisterPartition) : Nat :=
  rp.odPureAncillaQubits + rp.ancillaQubit

/--
Theorem 1-term Robin resource shape:
`O(sum_g Q_g n log n + kappa n)` gates and `2n` pure ancillas.
-/
def oneTermRobinResourceExpr : AsymptoticResource where
  gates :=
    (CostExpr.atom "sum_g(Q_g)") * (CostExpr.atom "n") * (CostExpr.log (CostExpr.atom "n")) +
    (CostExpr.atom "kappa") * (CostExpr.atom "n")
  pureAncilla := (2 : CostExpr) * CostExpr.atom "n"

/-- Number of deviating (boundary) indices: K1 + 2^n - K2.
The paper notes this is O(1) as it depends on the finite-difference accuracy order.
main.tex:1092-1095 --/
def deviatingIndices (K1 K2 gridSize : Nat) : Nat :=
  K1 + gridSize - K2

/--
Precise gate cost formula from the text (main.tex:1088-1089), before absorbing the
O(1) boundary deviation count into the Theorem's simplified formula.
`O(sum_g Q_g n log n + kappa * (K1 + 2^n - K2) * n)` gates.
The term `K1 + 2^n - K2` is the number of deviating rows, which is O(1).
main.tex:1088-1089 --/
def oneTermRobinPreciseResourceExpr : AsymptoticResource where
  gates :=
    (CostExpr.atom "sum_g(Q_g)") * (CostExpr.atom "n") * (CostExpr.log (CostExpr.atom "n")) +
    (CostExpr.atom "kappa") * (CostExpr.atom "(K1 + 2^n - K2)") * (CostExpr.atom "n")
  pureAncilla := (2 : CostExpr) * CostExpr.atom "n"

/-- deviatingIndices computes K1 + gridSize - K2, the number of boundary rows.
For the fourth-order stencil with K1=2, K2=gridSize(n)-3, this gives 2+3=5.
main.tex:1092-1095 --/
theorem deviatingIndices_example :
    deviatingIndices 2 (gridSize 3 - 3) (gridSize 3) = 5 := rfl

/-- Numeric resource useful for concrete search runs with fixed parameters. -/
def oneTermRobinResource (p : OneTermRobinParameters) : Resource :=
  Resource.ofCounts
    (p.polynomialDegreeCost * p.n * clog2 p.n + p.kappa * p.n)
    0
    (2 * p.n)

theorem oneTermRobin_pureAncilla (p : OneTermRobinParameters) :
    (oneTermRobinResource p).pureAncilla = 2 * p.n := rfl

/--
Register layout for the one-term Robin block encoding.
Signal qubits = ⌈log₂ n⌉ + ⌈log₂ G_f⌉ + ⌈log₂ κ⌉ + 4
match the paper's Theorem (main.tex:1098-1109).
System qubits address `n` grid points; pure ancillas are workspace.
-/
def oneTermRobinLayout (p : OneTermRobinParameters) : RegisterLayout where
  systemQubits := clog2 (gridSize p.n)
  signalQubits := clog2 p.n + clog2 p.functionPieces + clog2 p.kappa + 4
  pureAncillas := 2 * p.n

/--
Placeholder circuit for the one-term Robin block encoding.
Gate order matches Fig. 1_term_ROBIN (main.tex:1125-1163):
  1. U_indic sets bulk/boundary indicator ancilla.
  2. O_DT^S encodes D^T amplitudes (bulk) via sparse-amplitude oracle.
  3. Ry_boundary applies controlled rotations for boundary entries.
  4. O_D^BS is the banded-sparse-access oracle for D.
  5. O_f encodes f(x_j) via amplitude oracle.
  6. SWAP between two n-qubit registers.
  7. (O_D^BS)^† uncomputes the sparse-access register.
Oracle names match `defaultRobinCircuitSkeleton` field values.
figure:1_term_ROBIN --/
def oneTermRobinCircuit : Circuit :=
  [ Gate.oracleCall "U_indic"
  , Gate.oracleCall "O_DT^S"
  , Gate.oracleCall "Ry_boundary"
  , Gate.oracleCall "O_D^BS"
  , Gate.oracleCall "O_f"
  , Gate.swap 0 0   -- placeholder qubit indices; SWAP is a native gate
  , Gate.oracleCall "(O_D^BS)^†"
  ]

/--
Theorem-facing Fig. 1-term Robin transcript.

This label list is the source-facing circuit map used by the conversion window.
It deliberately differs from the active seven-gate backend list: the backend
matrix product still uses `oneTermRobinCircuit`, while this transcript keeps
the sparse-register preparation sides, the explicit `U_indic^dagger` cleanup
slot, and the pre-SWAP `O_DT^BS` label visible for paper audit.
figure:1_term_ROBIN, eq:arbitrary sparcity --/
def oneTermRobinTheoremFacingFig4Circuit : Circuit :=
  [ Gate.oracleCall "H_W^(kappa)"
  , Gate.oracleCall "U_indic"
  , Gate.oracleCall "O_DT^S"
  , Gate.oracleCall "Ry_boundary"
  , Gate.oracleCall "O_DT^BS"
  , Gate.oracleCall "U_indic^dagger"
  , Gate.oracleCall "O_f"
  , Gate.swap 0 0
  , Gate.oracleCall "(O_D^BS)^dagger"
  , Gate.oracleCall "(H_W^(kappa))^dagger"
  ]

/--
The theorem-facing transcript exposes the source-correction slots explicitly.

This theorem is a transcript guard only.  It does not replace
`oneTermRobinCircuit`, does not change `oneTermRobinGateMatrixPlaceholders`, and
does not promote any oracle correctness or unitarity flag.
-/
theorem oneTermRobinTheoremFacingFig4Circuit_gateList :
    oneTermRobinTheoremFacingFig4Circuit =
      [ Gate.oracleCall "H_W^(kappa)"
      , Gate.oracleCall "U_indic"
      , Gate.oracleCall "O_DT^S"
      , Gate.oracleCall "Ry_boundary"
      , Gate.oracleCall "O_DT^BS"
      , Gate.oracleCall "U_indic^dagger"
      , Gate.oracleCall "O_f"
      , Gate.swap 0 0
      , Gate.oracleCall "(O_D^BS)^dagger"
      , Gate.oracleCall "(H_W^(kappa))^dagger"
      ] := rfl

/--
The active backend circuit remains the seven-gate product currently used by
the finite matrix semantics.

Theorem-facing proof maps must not call this list the full Fig. 1-term Robin
transcript, because it omits both `H_W^(kappa)` sides and the explicit
`U_indic^dagger` source slot.
-/
theorem oneTermRobinActiveBackendCircuit_gateList :
    oneTermRobinCircuit =
      [ Gate.oracleCall "U_indic"
      , Gate.oracleCall "O_DT^S"
      , Gate.oracleCall "Ry_boundary"
      , Gate.oracleCall "O_D^BS"
      , Gate.oracleCall "O_f"
      , Gate.swap 0 0
      , Gate.oracleCall "(O_D^BS)^†"
      ] := rfl

/-- Symbolic normalizer α = N_D · N_f · κ for the one-term Robin construction. -/
def oneTermRobinNormalizer : Coeff :=
  Coeff.mul (Coeff.mul (Coeff.symbol "N_D") (Coeff.symbol "N_f")) (Coeff.symbol "kappa")

/--
Block-encoding spec for the one-term Robin derivative operator.
Takes the target matrix as a parameter so the spec is reusable across different
stencil choices and boundary data without creating import cycles.
Normalizer: symbolic `N_D · N_f · κ`.
Error: zero (exact encoding, no approximation yet).
-/
def oneTermRobinSpec (p : OneTermRobinParameters)
    (mat : Matrix (gridSize p.n) (gridSize p.n) Coeff) :
    BlockEncodingSpec Coeff (gridSize p.n) (gridSize p.n) where
  matrix := mat
  normalizer := oneTermRobinNormalizer
  error := Coeff.rat 0
  layout := oneTermRobinLayout p
  circuit := oneTermRobinCircuit
  resource := oneTermRobinResource p

/-- The spec's pure ancilla matches the resource formula. -/
theorem oneTermRobinSpec_ancilla (p : OneTermRobinParameters)
    (mat : Matrix (gridSize p.n) (gridSize p.n) Coeff) :
    (oneTermRobinSpec p mat).resource.pureAncilla = 2 * p.n := rfl

/--
The spec's circuit local cost: the SWAP placeholder costs 3 CNOTs and each
unexpanded oracle call is counted as one unresolved call in the candidate score.
figure:1_term_ROBIN
-/
theorem oneTermRobinSpec_circuitCost :
    Circuit.resource oneTermRobinCircuit = Resource.ofCountsWithDepth 0 3 6 0 9 := rfl

/-- Evaluating the symbolic normalizer `N_D · N_f · κ` under an environment gives
the product of the three symbol values. -/
@[simp] theorem oneTermRobinNormalizer_eval (env : String → Rat) :
    Coeff.evalWith env oneTermRobinNormalizer = env "N_D" * env "N_f" * env "kappa" := by
  simp [oneTermRobinNormalizer]

/-- The paper's one-term Robin block-encoding construction claim. -/
def oneTermRobinClaim : ConstructionClaim where
  name := "one-term-robin-block-encoding"
  source := "Guseynov-Huang-Liu 2025, Theorem one-term block-encoding"
  target := "A_k = f(x) * d^m/dx^m with Robin boundary corrections"
  normalization := "N_D * N_f * kappa"
  layout := "ceil(log2 n) + ceil(log2 G_f) + ceil(log2 kappa) + 4 signal qubits, 2n pure ancillas"
  resource := oneTermRobinResourceExpr

/-- One-dimensional Hamiltonian block-encoding resource shape. -/
def oneDimHamiltonianResourceExpr : AsymptoticResource where
  gates :=
    CostExpr.atom "sum_g(Q_v_g) * n * log(n)" +
    CostExpr.sum "k < eta" (CostExpr.atom "kappa_k * n + sum_g(Q_fkg) * n * log(n)") +
    CostExpr.atom "n_xi * log(n_xi)"
  pureAncilla := (2 : CostExpr) * CostExpr.atom "n" + (2 : CostExpr)

/-- The paper's 1D Hamiltonian block-encoding construction claim. -/
def oneDimHamiltonianClaim : ConstructionClaim where
  name := "one-dimensional-pde-hamiltonian-block-encoding"
  source := "Guseynov-Huang-Liu 2025, Theorem one-dimensional block-encoding"
  target := "H = S1 tensor x_xi + S2 tensor I_xi"
  normalization := "O(kappa * ||H||_max)"
  layout := "ceil(log2 n_xi)+ceil(log2 n)+ceil(log2 G)+ceil(log2 kappa)+ceil(log2 eta)+7 signal qubits"
  resource := oneDimHamiltonianResourceExpr

/-- Multidimensional Hamiltonian block-encoding resource shape. -/
def multiDimHamiltonianResourceExpr : AsymptoticResource where
  gates :=
    CostExpr.atom "M * Q_PET * G * Q * (d*n*log(n)+n_s*log(n_s))" +
    CostExpr.atom "n_xi * log(n_xi)" +
    CostExpr.atom "d * eta * kappa * n"
  pureAncilla := CostExpr.atom "O(n)"

/-- The paper's multidimensional Hamiltonian block-encoding construction claim. -/
def multiDimHamiltonianClaim : ConstructionClaim where
  name := "multidimensional-pde-hamiltonian-block-encoding"
  source := "Guseynov-Huang-Liu 2025, Theorem multi-dimensional block-encoding"
  target := "H = I tensor p_s tensor I_xi + S1^(d) tensor x_xi + S2^(d) tensor I_xi"
  normalization := "O(kappa * ||H||_max)"
  layout := "d*ceil(log2 n)+ceil(log2 n_s)+ceil(log2 n_xi)+ceil(log2 G)+ceil(log2 kappa)+ceil(log2 eta)+ceil(log2 M)+4d+5 signal qubits"
  resource := multiDimHamiltonianResourceExpr

/-- A proof obligation tracked by description and paper source anchor.
`proved` is `Bool` (not `Prop`) so that unproved obligations are honest data,
not mathematically false claims. main.tex --/
structure ObligationRecord where
  description : String
  source : String
  proved : Bool := false
deriving Repr, DecidableEq

/-- Circuit skeleton matching Fig. 1_term_ROBIN (main.tex:1137-1167).
Each field corresponds to a labeled box or operation in the figure.
All oracles are recorded as symbolic names; their implementation is delegated
to separate oracle-contract structures. figure:1_term_ROBIN --/
structure RobinCircuitSkeleton where
  /-- Bulk/boundary indicator unitary U_indic(K1,K2). main.tex:1088-1099 --/
  indicatorOracle : String
  /-- Bulk window lower bound K1. main.tex:1095 --/
  K1 : Nat
  /-- Bulk window upper bound K2. main.tex:1095 --/
  K2 : Nat
  /-- Sparse-amplitude oracle for transposed derivative D^T.
  Lemma 3 (main.tex:822-849). --/
  sparseAmplitudeOracleDT : String
  /-- Banded-sparse-access oracle for D. Lemma 1 (main.tex:784-801). --/
  bandedSparseAccessOracleD : String
  /-- Hermitian conjugate of the banded-sparse-access oracle (O_D^BS)^†.
  figure:1_term_ROBIN caption, main.tex:1148 --/
  bandedSparseAccessOracleD_dagger : String
  /-- Boundary-controlled R_y rotations with angles theta_j^s = arccos(D_j^(s)/N_D).
  main.tex:1115-1120 --/
  controlledRyBoundary : String
  /-- Amplitude oracle O_f for piecewise polynomial f(x). Thm 5 (main.tex:870-910). --/
  functionOracle : String
  /-- SWAP between two n-qubit registers. figure:1_term_ROBIN, main.tex:1140 --/
  swapOperation : String
  /-- Y-frame register merge (no quantum operation). figure:1_term_ROBIN caption --/
  mergeFrame : String
  /-- m_f = ceil(log2 n) + ceil(log2 G_f) + 3 qubits reserved for O_f. main.tex:1141 --/
  mfSignalQubits : Nat
  /-- ceil(log2 kappa) qubits for sparse indexing. figure:1_term_ROBIN caption --/
  kappaSignalQubits : Nat
  /-- n - ceil(log2 kappa) pure ancilla qubits for O_D^BS register.
  figure:1_term_ROBIN caption, main.tex:1149 --/
  pureAncillaODRegister : Nat
deriving Repr, DecidableEq

/-- Eq. ROBIN clarified, gamma_1 component (main.tex:1113).
State after U_indic sets the indicator ancilla.
The boundary and bulk summation terms have different normalizers:
  boundary: 1/(N_D · sqrt(kappa)), indicator |0>
  bulk:     1/sqrt(kappa),        indicator |1>
main.tex:1113 --/
structure RobinGamma1 where
  /-- Sparse index upper bound: s in {0, ..., kappa-1}. main.tex:1113 --/
  kappa : Nat
  /-- Bulk window lower bound. main.tex:1095, 1113 --/
  K1 : Nat
  /-- Bulk window upper bound. main.tex:1095, 1113 --/
  K2 : Nat
  /-- Grid size = 2^n. main.tex:1113 --/
  gridSize : Nat
  /-- Boundary normalizer N_D · sqrt(kappa) (symbolic).
  The boundary summation in gamma_1 is scaled by 1/(N_D · sqrt(kappa)). main.tex:1113 --/
  boundaryNormalizer : Coeff
  /-- Bulk normalizer sqrt(kappa) (symbolic).
  The bulk summation in gamma_1 is scaled by 1/sqrt(kappa) — notably
  without the N_D factor, because the sparse-amplitude oracle has not yet
  been applied. main.tex:1113 --/
  bulkNormalizer : Coeff
  /-- Number of m_f qubits reserved for O_f. main.tex:1141 --/
  mfQubits : Nat
deriving Repr, DecidableEq

/-- Eq. ROBIN clarified, gamma_2 component (main.tex:1115).
State after sparse-amplitude oracle encodes D^T values. main.tex:1115 --/
structure RobinGamma2 where
  /-- Sparse index upper bound. main.tex:1115 --/
  kappa : Nat
  /-- Bulk window lower bound. main.tex:1115 --/
  K1 : Nat
  /-- Bulk window upper bound. main.tex:1115 --/
  K2 : Nat
  /-- Grid size. main.tex:1115 --/
  gridSize : Nat
  /-- Normalization factor N_D * sqrt(kappa) (symbolic). main.tex:1115 --/
  normalizer : Coeff
  /-- Whether this includes the orthogonal remainder "+ ...". main.tex:1115 --/
  hasOrthogonalRemainder : Bool
deriving Repr, DecidableEq

/-- Eq. ROBIN clarified, gamma_3 component (main.tex:1117).
State after O_f encodes f(x_j) values. main.tex:1117 --/
structure RobinGamma3 where
  /-- Sparse index upper bound. main.tex:1117 --/
  kappa : Nat
  /-- Bulk window lower bound. main.tex:1117 --/
  K1 : Nat
  /-- Bulk window upper bound. main.tex:1117 --/
  K2 : Nat
  /-- Grid size. main.tex:1117 --/
  gridSize : Nat
  /-- Normalization factor N_D * N_f * kappa (symbolic). main.tex:1117 --/
  normalizer : Coeff
  /-- Whether this includes the orthogonal remainder "+ ...". main.tex:1117 --/
  hasOrthogonalRemainder : Bool
  /-- Number of pure ancilla qubits identified: n - ceil(log2 kappa) + 1. main.tex:1117, 1149 --/
  pureAncillaQubits : Nat
deriving Repr, DecidableEq

/-- Bundle of the three intermediate wavefunction states from Eq. ROBIN clarified.
Captures the full circuit state evolution from input through U_indic, O_DT^S, and O_f.
main.tex:1113-1117, figure:1_term_ROBIN --/
structure RobinWavefunctionDecomposition where
  /-- gamma_1: state after U_indic. main.tex:1113 --/
  gamma1 : RobinGamma1
  /-- gamma_2: state after sparse-amplitude oracle. main.tex:1115 --/
  gamma2 : RobinGamma2
  /-- gamma_3: state after function oracle O_f. main.tex:1117 --/
  gamma3 : RobinGamma3
  /-- The shared sparse index upper bound. --/
  kappa : Nat
  /-- The shared bulk window lower bound. --/
  K1 : Nat
  /-- The shared bulk window upper bound. --/
  K2 : Nat
  /-- The shared grid size 2^n. --/
  gridSize : Nat
deriving Repr, DecidableEq

/-- Default wavefunction decomposition from concrete parameters.
figure:1_term_ROBIN, main.tex:1113-1117 --/
def defaultRobinWavefunctionDecomposition (p : OneTermRobinParameters) : RobinWavefunctionDecomposition where
  gamma1 := {
    kappa := p.kappa
    K1 := 2
    K2 := gridSize p.n - 3
    gridSize := gridSize p.n
    boundaryNormalizer := Coeff.mul (Coeff.symbol "N_D") (Coeff.symbol "sqrt(kappa)")
    bulkNormalizer := Coeff.symbol "sqrt(kappa)"
    mfQubits := clog2 p.n + clog2 p.functionPieces + 3
  }
  gamma2 := {
    kappa := p.kappa
    K1 := 2
    K2 := gridSize p.n - 3
    gridSize := gridSize p.n
    normalizer := Coeff.mul (Coeff.symbol "N_D") (Coeff.symbol "sqrt(kappa)")
    hasOrthogonalRemainder := true
  }
  gamma3 := {
    kappa := p.kappa
    K1 := 2
    K2 := gridSize p.n - 3
    gridSize := gridSize p.n
    normalizer := Coeff.mul (Coeff.mul (Coeff.symbol "N_D") (Coeff.symbol "N_f")) (Coeff.symbol "kappa")
    hasOrthogonalRemainder := true
    pureAncillaQubits := p.n - clog2 p.kappa + 1
  }
  kappa := p.kappa
  K1 := 2
  K2 := gridSize p.n - 3
  gridSize := gridSize p.n

/-- Bundle of proof obligations for the one-term Robin block encoding.
Each obligation references a specific claim in the paper and tracks whether
it has been formally proved. None are proved in the current version.
Guseynov-Huang-Liu 2025, one-term Robin theorem, arXiv:2506.20478. --/
structure RobinProofObligations where
  /-- U_indic is unitary and implements the bulk-window predicate. --/
  indicatorUnitary : ObligationRecord := {
    description := "U_indic(K1,K2) implements the bulk/boundary indicator correctly"
    source := "Guseynov-Huang-Liu 2025, U_indic definition and Fig. 1-term Robin, arXiv:2506.20478"
    proved := false
  }
  /-- Sparse-amplitude oracle O_D^S is unitary and encodes D^(s)/N_D. --/
  sparseAmplitudeOracleCorrect : ObligationRecord := {
    description := "O_DT^S prepares the D^T sparse-amplitude branch D_j^(s)/N_D from Lemma 3, Eq. (20)"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  /-- Banded-sparse-access oracle O_D^BS is unitary and writes r_si. --/
  bandedSparseAccessCorrect : ObligationRecord := {
    description := "O_D^BS maps |0>^(n-l)|s>^l|i>^n to |r_si>^n|i>^n and supports dagger cleanup"
    source := "Guseynov-Huang-Liu 2025, Lemma 1 and Fig. 1-term Robin, arXiv:2506.20478"
    proved := false
  }
  /-- Function oracle O_f is unitary and block-encodes f(x_j)/N_f. --/
  functionOracleCorrect : ObligationRecord := {
    description := "O_f block-encodes the piecewise polynomial f(x) discretized on the grid"
    source := "Guseynov-Huang-Liu 2025, Theorem amplitude-oracle for piece-wise polynomial function and Fig. 1-term Robin, arXiv:2506.20478"
    proved := false
  }
  /-- Controlled R_y angles encode boundary D_j^(s)/N_D correctly. --/
  controlledRyCorrect : ObligationRecord := {
    description := "R_y rotation angles theta_j^s = arccos(D_j^(s)/N_D) are correct"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and boundary Ry angle formula, arXiv:2506.20478"
    proved := false
  }
  /-- Full circuit U_Ak^(1) is unitary. --/
  circuitUnitary : ObligationRecord := {
    description := "The full one-term Robin circuit U_Ak^(1) is unitary"
    source := "Guseynov-Huang-Liu 2025, one-term Robin theorem, arXiv:2506.20478"
    proved := false
  }
  /-- Block extraction: (⟨0|⊗I) U (|0⟩⊗I) = A_k / (N_D * N_f * kappa). --/
  blockExtraction : ObligationRecord := {
    description := "Block extraction yields A_k / alpha where alpha = N_D * N_f * kappa"
    source := "Guseynov-Huang-Liu 2025, one-term Robin theorem, arXiv:2506.20478"
    proved := false
  }
  /-- Resource bound: O(sum Q_g n log n + kappa n) gates, 2n pure ancillas. --/
  resourceBound : ObligationRecord := {
    description := "Gate count O(sum_g Q_g n log n + kappa n), pure ancillas 2n"
    source := "Guseynov-Huang-Liu 2025, one-term Robin theorem resource claim, arXiv:2506.20478"
    proved := false
  }
  /-- Pure ancilla cleanup: 2n ancillas returned to |0⟩. figure:1_term_ROBIN caption --/
  ancillaCleanup : ObligationRecord := {
    description := "All 2n pure ancilla qubits are returned to |0⟩ state"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin caption, arXiv:2506.20478"
    proved := false
  }
  /-- Ghost-point elimination yields correct Robin boundary row coefficients. --/
  ghostPointElimination : ObligationRecord := {
    description := "Ghost-point elimination via Robin boundary relation produces correct boundary rows"
    source := "Guseynov-Huang-Liu 2025, Robin boundary-row derivation, arXiv:2506.20478"
    proved := false
  }
deriving Repr, DecidableEq

/-- Default circuit skeleton for the one-term Robin construction,
with oracle names matching the paper's notation. figure:1_term_ROBIN --/
def defaultRobinCircuitSkeleton (p : OneTermRobinParameters) : RobinCircuitSkeleton where
  indicatorOracle := "U_indic"
  K1 := 2  -- depends on stencil accuracy order; main.tex:1095
  K2 := gridSize p.n - 3  -- symmetric boundary; main.tex:1095
  sparseAmplitudeOracleDT := "O_DT^S"
  bandedSparseAccessOracleD := "O_D^BS"
  bandedSparseAccessOracleD_dagger := "(O_D^BS)^†"
  controlledRyBoundary := "Ry_boundary"
  functionOracle := "O_f"
  swapOperation := "SWAP"
  mergeFrame := "merge"
  mfSignalQubits := clog2 p.n + clog2 p.functionPieces + 3
  kappaSignalQubits := clog2 p.kappa
  pureAncillaODRegister := p.n - clog2 p.kappa

/--
Paper-level source contract for the banded sparse-access oracle in Lemma 1.

The input register is the padded sparse-index register
`|0>^(n-l)|s>^l` followed by the row register `|i>^n`; the output is
`|r_si>^n|i>^n`.  This record is intentionally separate from the current
`bandedSparseAccessMatrix` helper, which overwrites the system register with a
Robin column map and therefore does not yet implement this paper contract.
Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478. -/
structure BandedSparseAccessPaperContract where
  sourceAnchor : String
  rowRegisterQubits : Nat
  paddedZeroQubits : Nat
  sparseIndexQubits : Nat
  outputAddressQubits : Nat
  inputKet : String
  outputKet : String
  imageFormula : String
  cleanInputDomain : ObligationRecord
  widthCompatible : ObligationRecord
  addressRange : ObligationRecord
  noSpill : ObligationRecord
  forwardCorrect : ObligationRecord
  daggerCleanup : ObligationRecord
  unitaryExtension : ObligationRecord
deriving Repr, DecidableEq

/--
Default Lemma 1 register contract for the one-term Robin parameters.

The `widthCompatible` obligation stays explicit because the current parameter
type does not enforce `clog2 kappa <= n`; faithful proofs should discharge that
side condition or specialize to a parameter family where it is available.
-/
def defaultBandedSparseAccessPaperContract
    (p : OneTermRobinParameters) : BandedSparseAccessPaperContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
  rowRegisterQubits := p.n
  paddedZeroQubits := p.n - clog2 p.kappa
  sparseIndexQubits := clog2 p.kappa
  outputAddressQubits := p.n
  inputKet := "|0>^(n-l)|s>^l|i>^n"
  outputKet := "|r_si>^n|i>^n"
  imageFormula := "r_si = r_s0 + i mod 2^n"
  cleanInputDomain := {
    description := "Lemma 1 source equation applies to columns whose padded zero register is |0>^(n-l)"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }
  widthCompatible := {
    description := "padded zero register plus sparse-index register has width n"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }
  addressRange := {
    description := "the written address r_si is an n-bit value before it is placed in the O_D^BS register"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }
  noSpill := {
    description := "bandedSparseAccessPaperImage changes only the n-bit O_D^BS address register and does not spill into indicator or m_f bits"
    source := "Guseynov-Huang-Liu 2025, Lemma 1 and Fig. 1-term Robin, arXiv:2506.20478"
    proved := false
  }
  forwardCorrect := {
    description := "O_D^BS maps |0>^(n-l)|s>^l|i>^n to |r_si>^n|i>^n"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }
  daggerCleanup := {
    description := "(O_D^BS)^dagger cleans the padded sparse-index register after SWAP"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Lemma 1, arXiv:2506.20478"
    proved := false
  }
  unitaryExtension := {
    description := "extend the Lemma 1 clean-input image to a full unitary on non-clean padded-register columns"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- Contract for the derivative oracle O_D: sparse-access oracle for the banded
stencil matrix. Records stencil metadata, bandwidth, and a correctness obligation. main.tex:784-801 --/
structure DerivativeOracleContract (n : Nat) where
  stencil : Stencil
  bandwidth : Nat
  matrix : Matrix (gridSize n) (gridSize n) Coeff
  /-- Obligation: O_D^BS correctly maps sparse indices to matrix entries.
  main.tex:784-801 --/
  sparseCorrect : ObligationRecord
  bandwidth_eq : bandwidth = stencil.width

/-- Contract for the function oracle O_f: amplitude oracle encoding f(x) on the
grid. Records the piece count, normalization bound, and a correctness obligation. main.tex:870-910 -/
structure FunctionOracleContract (n : Nat) where
  functionPieces : Nat
  normalizerBound : Coeff
  /-- Obligation: O_f correctly block-encodes f(x_j)/N_f on the grid.
  main.tex:870-910 --/
  amplitudeCorrect : ObligationRecord

/-- Resource for the derivative oracle O_D using the banded sparse-access formula
from Lemma 1 of Guseynov-Huang-Liu 2025. The half-bandwidth parameter is
`stencil.leftRadius` (assumes a symmetric stencil where leftRadius = rightRadius). -/
def derivativeOracleResource (n : Nat) (s : Stencil) : Resource :=
  bandedSparseAccessResource n s.leftRadius

/-- The derivative oracle's pure ancilla count is n - 1 (from Lemma 1). -/
@[simp] theorem derivativeOracleResource_pureAncilla (n : Nat) (s : Stencil) :
    (derivativeOracleResource n s).pureAncilla = n - 1 := rfl

/-- Typed theorem data for Theorem one-term block-encoding (main.tex:1098-1109).
Captures the exact block-encoding tuple (α, m, a) from the paper:
  α = N_D · N_f · κ    (normalizer)
  m = ⌈log₂ n⌉ + ⌈log₂ G_f⌉ + ⌈log₂ κ⌉ + 4   (signal ancilla qubits)
  a = 0                (zero approximation error)
along with the gate-count and pure-ancilla resource claims. -/
structure OneTermRobinTheoremData where
  /-- Block-encoding normalizer α = N_D · N_f · κ. main.tex:1102 --/
  alpha : Coeff
  /-- Signal ancilla qubits m = ⌈log₂ n⌉ + ⌈log₂ G_f⌉ + ⌈log₂ κ⌉ + 4. main.tex:1102 --/
  signalQubits : Nat
  /-- Approximation error a = 0 (exact block encoding). main.tex:1098-1109 --/
  error : Coeff
  /-- Gate-count bound: O(∑_g Q_g n log n + κ n). main.tex:1105-1108 --/
  gatesBound : String
  /-- Pure ancilla qubits: 2n. main.tex:1107 --/
  pureAncillas : Nat
  /-- All proof obligations for this theorem. main.tex:1098-1109 --/
  obligations : RobinProofObligations
deriving Repr, DecidableEq

/-- Default theorem data instance from concrete parameters. main.tex:1098-1109 --/
def defaultOneTermRobinTheoremData (p : OneTermRobinParameters) : OneTermRobinTheoremData where
  alpha := oneTermRobinNormalizer
  signalQubits := clog2 p.n + clog2 p.functionPieces + clog2 p.kappa + 4
  error := Coeff.rat 0
  gatesBound := "O(sum_g Q_g n log n + kappa n)"
  pureAncillas := 2 * p.n
  obligations := {}

/--
A controlled R_y rotation angle for a single boundary row entry.
The paper (Eq. angles for Ry, main.tex:1081-1083) defines:
  theta_j^s = arccos(D_j^(s) / N_D)
for sparse index s in {0,...,kappa-1} and boundary row j.
main.tex:1081-1083 --/
structure RobinBoundaryRotationAngle where
  /-- Row index j (boundary row: j < K1 or j > K2). main.tex:1082 --/
  row : Nat
  /-- Sparse index s in {0,...,kappa-1}. main.tex:1082 --/
  sparseIndex : Nat
  /-- The matrix entry D_j^(s) being encoded. main.tex:1082 --/
  matrixEntry : Coeff
  /-- The argument to arccos: D_j^(s) / N_D (symbolic Coeff).
  The caller must ensure this evaluates to a value in [-1, 1].
  main.tex:1081-1083 --/
  arccosArgument : Coeff
deriving Repr, DecidableEq

/--
The set of all boundary-controlled rotation angles for a given Robin construction.
For each boundary row j and sparse index s, there is one angle theta_j^s.
Total count = kappa * (K1 + gridSize - K2) = kappa * deviatingIndices.
main.tex:1081-1083, 1088-1089 --/
structure RobinBoundaryRotationSet where
  /-- Bulk window lower bound. main.tex:1095 --/
  K1 : Nat
  /-- Bulk window upper bound. main.tex:1095 --/
  K2 : Nat
  /-- Grid size = 2^n. main.tex:1082 --/
  gridSize : Nat
  /-- Diagonal sparsity bound (number of nonzero entries per row). main.tex:1075 --/
  kappa : Nat
  /-- Normalizer N_D >= ||D||_max. main.tex:1085 --/
  normalizerND : Coeff
  /-- Individual rotation angles, one per (boundary_row, sparse_index) pair.
  main.tex:1081-1083 --/
  angles : List RobinBoundaryRotationAngle
deriving Repr, DecidableEq

/--
Number of boundary rows = K1 + gridSize - K2.
Each boundary row has kappa rotation angles (one per sparse index).
main.tex:1092-1095 --/
def RobinBoundaryRotationSet.expectedCount (rs : RobinBoundaryRotationSet) : Nat :=
  rs.kappa * deviatingIndices rs.K1 rs.K2 rs.gridSize

def importedClaims : List ConstructionClaim :=
  [oneTermRobinClaim, oneDimHamiltonianClaim, multiDimHamiltonianClaim]

/-! ## Gate matrix placeholders for the one-term Robin circuit

Each gate in `oneTermRobinCircuit` gets a placeholder `GateMatrix` record.
The placeholder matrices are identity matrices on the full Hilbert space;
each carries a `SemanticObligation` with `proved := false` tracking that
the real matrix implementation is still pending.
figure:1_term_ROBIN, main.tex:1125-1163 --/

/--
Total number of qubits in the one-term Robin circuit.
Uses the register partition total: sum of all register widths.
main.tex:1098-1109 --/
def oneTermRobinTotalQubits (p : OneTermRobinParameters) : Nat :=
  (defaultRobinRegisterPartition p).totalQubits

/--
Effective signal qubits: total circuit qubits minus the system register width.
This is the number of non-system qubits in the register partition.
main.tex:1098-1109 --/
def effectiveRobinSignalQubits (p : OneTermRobinParameters) : Nat :=
  (defaultRobinRegisterPartition p).totalQubits - clog2 (gridSize p.n)

/--
The theorem tuple uses the paper's signal-qubit count.

This is the block-encoding parameter
`ceil(log2 n) + ceil(log2 G_f) + ceil(log2 kappa) + 4`, not the number of
all non-system wires in the concrete circuit register partition.
Guseynov-Huang-Liu 2025, Theorem one-term block-encoding,
arXiv:2506.20478.
-/
theorem defaultOneTermRobinTheoremData_signalQubits_eq_layout
    (p : OneTermRobinParameters) :
    (defaultOneTermRobinTheoremData p).signalQubits =
      (oneTermRobinLayout p).signalQubits := rfl

/--
The theorem tuple and the reusable layout record carry the same `2n`
pure-ancilla resource count.
-/
theorem defaultOneTermRobinTheoremData_pureAncillas_eq_layout
    (p : OneTermRobinParameters) :
    (defaultOneTermRobinTheoremData p).pureAncillas =
      (oneTermRobinLayout p).pureAncillas := rfl

/--
The theorem tuple and concrete resource record carry the same `2n`
pure-ancilla count.
-/
theorem defaultOneTermRobinTheoremData_pureAncillas_eq_resource
    (p : OneTermRobinParameters) :
    (defaultOneTermRobinTheoremData p).pureAncillas =
      (oneTermRobinResource p).pureAncilla := rfl

/--
The concrete block projection has to project all non-system wires.

Compared with the theorem-level signal parameter, the circuit-level projection
also includes the visible padded `O_D^BS` pure-register qubits and the trailing
one-qubit ancilla in the register partition.  This is an arithmetic bridge
between the theorem tuple and the matrix backend, not a block-correctness
proof.
-/
theorem effectiveRobinSignalQubits_eq_layout_signal_plus_visibleWorkspace
    (p : OneTermRobinParameters) :
    effectiveRobinSignalQubits p =
      (oneTermRobinLayout p).signalQubits +
        (defaultRobinRegisterPartition p).odPureAncillaQubits + 1 := by
  simp [effectiveRobinSignalQubits, oneTermRobinLayout,
    defaultRobinRegisterPartition, RobinRegisterPartition.totalQubits,
    clog2_gridSize]
  omega

/--
Same projection bridge, stated directly against the theorem-data tuple.

This pins the matrix backend's projection dimension to the paper theorem's
signal parameter plus the visible padded `O_D^BS` workspace and the one-qubit
ancilla.  It is still only a layout bridge, not an ancilla-cleanup or block
correctness proof.
-/
theorem effectiveRobinSignalQubits_eq_theoremData_signal_plus_visibleWorkspace
    (p : OneTermRobinParameters) :
    effectiveRobinSignalQubits p =
      (defaultOneTermRobinTheoremData p).signalQubits +
        (defaultRobinRegisterPartition p).odPureAncillaQubits + 1 := by
  rw [effectiveRobinSignalQubits_eq_layout_signal_plus_visibleWorkspace,
    defaultOneTermRobinTheoremData_signalQubits_eq_layout]

/--
Bit position of the indicator qubit in the compound register.
= ancillaQubit + systemQubits + odPureAncillaQubits + sparseIndexQubits
= 1 + n + (n - clog2 κ) + clog2 κ = 1 + 2n
main.tex:1113 --/
def robinIndicatorBitPosition (p : OneTermRobinParameters) : Nat :=
  let rp := defaultRobinRegisterPartition p
  rp.ancillaQubit + rp.systemQubits + rp.odPureAncillaQubits + rp.sparseIndexQubits

/--
Column mapping for the banded sparse access oracle O_D^BS.
Returns the column index for sparse index s in row i of the Robin derivative matrix.

For bulk rows (K1 ≤ i ≤ K2): 5 entries, col(s,i) = i - 2 + s for s < 5.
For left boundary:
  - Row 0 (3 entries): col(s,0) = s for s < 3
  - Row 1 (4 entries): col(s,1) = s for s < 4
For right boundary (N = gridSize n):
  - Row N-2 (4 entries): col(s,N-2) = N-4+s for s < 4
  - Row N-1 (3 entries): col(s,N-1) = N-3+s for s < 3
For unused sparse indices (s ≥ entry count): returns i (identity on system register).
main.tex:784-801 --/
def robinSparseColumnMap (n s i : Nat) : Nat :=
  let N := gridSize n
  let K1 := 2
  let K2 := N - 3
  if K1 ≤ i ∧ i ≤ K2 then
    if s < 5 then i - 2 + s else i
  else if i = 0 then
    if s < 3 then s else i
  else if i = 1 then
    if s < 4 then s else i
  else if i = N - 2 then
    if s < 4 then N - 4 + s else i
  else if i = N - 1 then
    if s < 3 then N - 3 + s else i
  else i

/--
Global sparse-slot offset table for the one-term Robin `κ = 7` construction.

The first five slots keep the existing fourth-order stencil order
`{-2,-1,0,1,2}`.  The final two slots record the boundary-effect diagonals
`{-3,3}` required by the source audit.  The active Lemma 1 address uses this
global slot table; row-dependent branch deletion remains only a rejected-model
helper.
Guseynov-Huang-Liu 2025, Lemma `Diagonal sparsity`, Lemma
`Banded-sparse-access-oracle`, and Remark `sparsity maximum`,
arXiv:2506.20478.
-/
def oneTermRobinGlobalSparseOffset (n s : Nat) : Nat :=
  let N := gridSize n
  match s with
  | 0 => N - 2
  | 1 => N - 1
  | 2 => 0
  | 3 => 1
  | 4 => 2
  | 5 => N - 3
  | 6 => 3
  | _ => 0

/--
Global sparse-access address `r_{si}=r_{s0}+i mod 2^n`.

This is the active paper address for `O_D^BS`; it does not remove zero
boundary-amplitude slots from the sparse register.
-/
def oneTermRobinGlobalSparseAddress (n s i : Nat) : Nat :=
  (oneTermRobinGlobalSparseOffset n s + i) % gridSize n

/-- The global sparse-slot address is always an `n`-bit row address. -/
theorem oneTermRobinGlobalSparseAddress_lt_gridSize
    (n s i : Nat) :
    oneTermRobinGlobalSparseAddress n s i < gridSize n := by
  unfold oneTermRobinGlobalSparseAddress
  exact Nat.mod_lt _ (by
    simp [gridSize]
    exact Nat.pow_pos (by decide : 0 < 2))

/--
Inverse sparse slot used by the post-SWAP cleanup candidate for the global
offset table.

This is only an executable preimage witness helper.  It does not assert
inverse uniqueness or promote the dagger-cleanup obligation.
-/
def oneTermRobinGlobalSparseInverseSlot (s : Nat) : Nat :=
  match s with
  | 0 => 4
  | 1 => 3
  | 2 => 2
  | 3 => 1
  | 4 => 0
  | 5 => 6
  | 6 => 5
  | _ => 2

/-- The global inverse-slot helper fits in the three-bit sparse register. -/
theorem oneTermRobinGlobalSparseInverseSlot_lt_eight (s : Nat) :
    oneTermRobinGlobalSparseInverseSlot s < 8 := by
  unfold oneTermRobinGlobalSparseInverseSlot
  split <;> decide

/-- The inverse sparse-slot helper stays in the active seven-slot table. -/
theorem oneTermRobinGlobalSparseInverseSlot_lt_seven
    {s : Nat} (hs : s < 7) :
    oneTermRobinGlobalSparseInverseSlot s < 7 := by
  have hs_cases :
      s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
        s = 4 ∨ s = 5 ∨ s = 6 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [oneTermRobinGlobalSparseInverseSlot]

/--
The inverse sparse-slot helper is an involution on the active `κ = 7` slot
set.  This is a finite-table proof block for the global-source preimage route;
it does not prove uniqueness of the full `O_D^BS` matrix image.
-/
theorem oneTermRobinGlobalSparseInverseSlot_involutive_of_lt_seven
    {s : Nat} (hs : s < 7) :
    oneTermRobinGlobalSparseInverseSlot
        (oneTermRobinGlobalSparseInverseSlot s) = s := by
  have hs_cases :
      s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
        s = 4 ∨ s = 5 ∨ s = 6 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [oneTermRobinGlobalSparseInverseSlot]

/--
The inverse sparse-slot helper is injective on the active `κ = 7` slot set.

This feeds the later clean-preimage uniqueness proof for the corrected global
slot model, but it intentionally leaves the semantic cleanup and unitarity
obligations false.
-/
theorem oneTermRobinGlobalSparseInverseSlot_injective_of_lt_seven
    {s t : Nat} (hs : s < 7) (ht : t < 7)
    (h : oneTermRobinGlobalSparseInverseSlot s =
      oneTermRobinGlobalSparseInverseSlot t) :
    s = t := by
  have hsInv :=
    oneTermRobinGlobalSparseInverseSlot_involutive_of_lt_seven hs
  have htInv :=
    oneTermRobinGlobalSparseInverseSlot_involutive_of_lt_seven ht
  calc
    s = oneTermRobinGlobalSparseInverseSlot
          (oneTermRobinGlobalSparseInverseSlot s) := hsInv.symm
    _ = oneTermRobinGlobalSparseInverseSlot
          (oneTermRobinGlobalSparseInverseSlot t) := by rw [h]
    _ = t := htInv

/--
Global sparse-address roundtrip for the supplied inverse-slot helper.

For an `n >= 3` grid and any encoded sparse value below `8`, addressing by a
slot and then by the inverse slot returns the original row modulo `2^n`.
This is the arithmetic block needed by the conditional post-SWAP preimage
candidate; it is not an injectivity or cleanup proof.
-/
theorem oneTermRobinGlobalSparseAddress_inverseSlot_address_eq
    {n s i : Nat} (hn : 3 ≤ n) (hs : s < 8) (hi : i < gridSize n) :
    oneTermRobinGlobalSparseAddress n (oneTermRobinGlobalSparseInverseSlot s)
        (oneTermRobinGlobalSparseAddress n s i) = i := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hs_cases :
      s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
        s = 4 ∨ s = 5 ∨ s = 6 ∨ s = 7 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · calc
      (2 + ((gridSize n - 2 + i) % gridSize n)) % gridSize n
          = (((gridSize n - 2 + i) % gridSize n) + 2) % gridSize n := by
            rw [Nat.add_comm]
      _ = (gridSize n - 2 + i + 2) % gridSize n := by
            rw [Nat.mod_add_mod]
      _ = (i + gridSize n) % gridSize n := by
            congr 1
            omega
      _ = i % gridSize n := by
            rw [Nat.add_mod_right]
      _ = i := Nat.mod_eq_of_lt hi
  · calc
      (1 + ((gridSize n - 1 + i) % gridSize n)) % gridSize n
          = (((gridSize n - 1 + i) % gridSize n) + 1) % gridSize n := by
            rw [Nat.add_comm]
      _ = (gridSize n - 1 + i + 1) % gridSize n := by
            rw [Nat.mod_add_mod]
      _ = (i + gridSize n) % gridSize n := by
            congr 1
            omega
      _ = i % gridSize n := by
            rw [Nat.add_mod_right]
      _ = i := Nat.mod_eq_of_lt hi
  · simpa [oneTermRobinGlobalSparseAddress, oneTermRobinGlobalSparseOffset,
      oneTermRobinGlobalSparseInverseSlot] using Nat.mod_eq_of_lt hi
  · calc
      (gridSize n - 1 + ((1 + i) % gridSize n)) % gridSize n
          = (((1 + i) % gridSize n) + (gridSize n - 1)) % gridSize n := by
            rw [Nat.add_comm]
      _ = (1 + i + (gridSize n - 1)) % gridSize n := by
            rw [Nat.mod_add_mod]
      _ = (i + gridSize n) % gridSize n := by
            congr 1
            omega
      _ = i % gridSize n := by
            rw [Nat.add_mod_right]
      _ = i := Nat.mod_eq_of_lt hi
  · calc
      (gridSize n - 2 + ((2 + i) % gridSize n)) % gridSize n
          = (((2 + i) % gridSize n) + (gridSize n - 2)) % gridSize n := by
            rw [Nat.add_comm]
      _ = (2 + i + (gridSize n - 2)) % gridSize n := by
            rw [Nat.mod_add_mod]
      _ = (i + gridSize n) % gridSize n := by
            congr 1
            omega
      _ = i % gridSize n := by
            rw [Nat.add_mod_right]
      _ = i := Nat.mod_eq_of_lt hi
  · calc
      (3 + ((gridSize n - 3 + i) % gridSize n)) % gridSize n
          = (((gridSize n - 3 + i) % gridSize n) + 3) % gridSize n := by
            rw [Nat.add_comm]
      _ = (gridSize n - 3 + i + 3) % gridSize n := by
            rw [Nat.mod_add_mod]
      _ = (i + gridSize n) % gridSize n := by
            congr 1
            omega
      _ = i % gridSize n := by
            rw [Nat.add_mod_right]
      _ = i := Nat.mod_eq_of_lt hi
  · calc
      (gridSize n - 3 + ((3 + i) % gridSize n)) % gridSize n
          = (((3 + i) % gridSize n) + (gridSize n - 3)) % gridSize n := by
            rw [Nat.add_comm]
      _ = (3 + i + (gridSize n - 3)) % gridSize n := by
            rw [Nat.mod_add_mod]
      _ = (i + gridSize n) % gridSize n := by
            congr 1
            omega
      _ = i % gridSize n := by
            rw [Nat.add_mod_right]
      _ = i := Nat.mod_eq_of_lt hi
  · simpa [oneTermRobinGlobalSparseAddress, oneTermRobinGlobalSparseOffset,
      oneTermRobinGlobalSparseInverseSlot] using Nat.mod_eq_of_lt hi

/-- If adding an in-range offset modulo `N` fixes an in-range index, the offset is zero. -/
private theorem mod_add_eq_self_imp_offset_zero
    {N a i : Nat} (ha : a < N) (hi : i < N)
    (h : (a + i) % N = i) : a = 0 := by
  by_cases hlt : a + i < N
  · have hmod : (a + i) % N = a + i := Nat.mod_eq_of_lt hlt
    omega
  · have hge : a + i ≥ N := by omega
    have hsum_lt : a + i < 2 * N := by omega
    have hsub_lt : a + i - N < N := by omega
    have hmod : (a + i) % N = a + i - N := by
      rw [Nat.mod_eq_sub_mod hge]
      exact Nat.mod_eq_of_lt hsub_lt
    omega

/-- If `a < 2N` and `a` is zero modulo `N`, then `a` is either `0` or `N`. -/
private theorem eq_zero_or_eq_base_of_mod_eq_zero_of_lt_two_mul
    {N a : Nat} (ha : a < 2 * N) (h : a % N = 0) :
    a = 0 ∨ a = N := by
  by_cases hlt : a < N
  · left
    have hmod : a % N = a := Nat.mod_eq_of_lt hlt
    omega
  · right
    have hge : a ≥ N := by omega
    have hsub_lt : a - N < N := by omega
    have hmod : a % N = a - N := by
      rw [Nat.mod_eq_sub_mod hge]
      exact Nat.mod_eq_of_lt hsub_lt
    omega

/-- Every active global sparse-slot offset is an `n`-bit address when `3 ≤ n`. -/
theorem oneTermRobinGlobalSparseOffset_lt_gridSize_of_lt_seven
    {n s : Nat} (hn : 3 ≤ n) (hs : s < 7) :
    oneTermRobinGlobalSparseOffset n s < gridSize n := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hs_cases :
      s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
        s = 4 ∨ s = 5 ∨ s = 6 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [oneTermRobinGlobalSparseOffset] <;> omega

/--
Composing two global sparse-slot addresses is addition by the sum of their
global offsets modulo the grid size.
-/
theorem oneTermRobinGlobalSparseAddress_comp_eq_mod_offset_sum
    {n s t i : Nat} :
    oneTermRobinGlobalSparseAddress n t
        (oneTermRobinGlobalSparseAddress n s i) =
      (((oneTermRobinGlobalSparseOffset n t +
          oneTermRobinGlobalSparseOffset n s) % gridSize n) + i) %
        gridSize n := by
  unfold oneTermRobinGlobalSparseAddress
  calc
    (oneTermRobinGlobalSparseOffset n t +
          ((oneTermRobinGlobalSparseOffset n s + i) % gridSize n)) %
        gridSize n
        = (((oneTermRobinGlobalSparseOffset n s + i) % gridSize n) +
            oneTermRobinGlobalSparseOffset n t) % gridSize n := by
          rw [Nat.add_comm]
    _ = (oneTermRobinGlobalSparseOffset n s + i +
            oneTermRobinGlobalSparseOffset n t) % gridSize n := by
          rw [Nat.mod_add_mod]
    _ = (oneTermRobinGlobalSparseOffset n t +
            oneTermRobinGlobalSparseOffset n s + i) % gridSize n := by
          congr 1
          omega
    _ = (((oneTermRobinGlobalSparseOffset n t +
            oneTermRobinGlobalSparseOffset n s) % gridSize n) + i) %
          gridSize n := by
          rw [Nat.mod_add_mod]

/--
If two active global sparse-slot offsets sum to zero modulo the grid, the first
slot is the reverse slot of the second.

This is only a finite arithmetic block for the corrected `O_D^BS` address
route; it does not prove dagger cleanup, unitarity, or block extraction.
-/
theorem oneTermRobinGlobalSparseOffset_sum_mod_eq_zero_unique_of_lt_seven
    {n s t : Nat} (hn : 3 ≤ n) (hs : s < 7) (ht : t < 7)
    (hzero :
      (oneTermRobinGlobalSparseOffset n t +
          oneTermRobinGlobalSparseOffset n s) % gridSize n = 0) :
    t = oneTermRobinGlobalSparseInverseSlot s := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hot :
      oneTermRobinGlobalSparseOffset n t < gridSize n :=
    oneTermRobinGlobalSparseOffset_lt_gridSize_of_lt_seven hn ht
  have hos :
      oneTermRobinGlobalSparseOffset n s < gridSize n :=
    oneTermRobinGlobalSparseOffset_lt_gridSize_of_lt_seven hn hs
  have hsum :
      oneTermRobinGlobalSparseOffset n t +
            oneTermRobinGlobalSparseOffset n s = 0 ∨
        oneTermRobinGlobalSparseOffset n t +
            oneTermRobinGlobalSparseOffset n s = gridSize n :=
    eq_zero_or_eq_base_of_mod_eq_zero_of_lt_two_mul (by omega) hzero
  have hs_cases :
      s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
        s = 4 ∨ s = 5 ∨ s = 6 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals
    have ht_cases :
        t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨
          t = 4 ∨ t = 5 ∨ t = 6 := by
      omega
    rcases ht_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl
    all_goals
      simp [oneTermRobinGlobalSparseOffset,
        oneTermRobinGlobalSparseInverseSlot] at hsum ⊢ <;> omega

/--
Uniqueness of the reverse sparse slot for the corrected global-slot address.

For active one-term Robin slots `s,t < 7`, if applying slot `t` after slot `s`
returns every in-range row `i`, then `t` must be the table inverse of `s`.
This feeds the future clean-preimage uniqueness route while leaving all
semantic `O_D^BS` proof flags false.
-/
theorem oneTermRobinGlobalSparseAddress_inverseSlot_unique_of_lt_seven
    {n s t i : Nat} (hn : 3 ≤ n) (hs : s < 7) (ht : t < 7)
    (hi : i < gridSize n)
    (h :
      oneTermRobinGlobalSparseAddress n t
          (oneTermRobinGlobalSparseAddress n s i) = i) :
    t = oneTermRobinGlobalSparseInverseSlot s := by
  have hNpos : 0 < gridSize n := by
    simp [gridSize]
    exact Nat.pow_pos (by decide : 0 < 2)
  have hcomp :=
    oneTermRobinGlobalSparseAddress_comp_eq_mod_offset_sum
      (n := n) (s := s) (t := t) (i := i)
  have hsumLt :
      (oneTermRobinGlobalSparseOffset n t +
          oneTermRobinGlobalSparseOffset n s) % gridSize n <
        gridSize n :=
    Nat.mod_lt _ hNpos
  have hzero :
      (oneTermRobinGlobalSparseOffset n t +
          oneTermRobinGlobalSparseOffset n s) % gridSize n = 0 :=
    mod_add_eq_self_imp_offset_zero hsumLt hi (by rwa [← hcomp])
  exact oneTermRobinGlobalSparseOffset_sum_mod_eq_zero_unique_of_lt_seven
    hn hs ht hzero

/--
For a fixed in-range row, the corrected seven-slot global address table is
injective in the sparse slot.

The proof reuses the reverse-slot uniqueness block rather than repeating the
finite offset table.  It is still only an address-level arithmetic lemma; it
does not promote any `O_D^BS` semantic flag.
-/
theorem oneTermRobinGlobalSparseAddress_same_row_injective_of_lt_seven
    {n s t i : Nat} (hn : 3 ≤ n) (hs : s < 7) (ht : t < 7)
    (hi : i < gridSize n)
    (h :
      oneTermRobinGlobalSparseAddress n s i =
        oneTermRobinGlobalSparseAddress n t i) :
    s = t := by
  have hround :
      oneTermRobinGlobalSparseAddress n
          (oneTermRobinGlobalSparseInverseSlot s)
          (oneTermRobinGlobalSparseAddress n t i) = i := by
    rw [← h]
    exact oneTermRobinGlobalSparseAddress_inverseSlot_address_eq
      (n := n) (s := s) (i := i) hn (by omega) hi
  have hinv :
      oneTermRobinGlobalSparseInverseSlot s =
        oneTermRobinGlobalSparseInverseSlot t :=
    oneTermRobinGlobalSparseAddress_inverseSlot_unique_of_lt_seven
      (n := n) (s := t) (t := oneTermRobinGlobalSparseInverseSlot s)
      (i := i) hn ht
      (oneTermRobinGlobalSparseInverseSlot_lt_seven hs) hi hround
  exact oneTermRobinGlobalSparseInverseSlot_injective_of_lt_seven
    hs ht hinv

/--
Row-dependent sparse-branch domain for the executable one-term Robin stencil.

This predicate is a source-contract correction candidate for Lemma 1
`O_D^BS`: it marks exactly the sparse indices that correspond to nonzero
stencil entries in the same five row regions used by `robinSparseColumnMap`.
The active matrix is not changed by this predicate; unused branches still
remain a separate unitary-extension obligation.
Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478.
-/
def robinSparseColumnBranchValid (n s i : Nat) : Bool :=
  let N := gridSize n
  if 2 ≤ i ∧ i ≤ N - 3 then
    decide (s < 5)
  else if i = 0 then
    decide (s < 3)
  else if i = 1 then
    decide (s < 4)
  else if i = N - 2 then
    decide (s < 4)
  else if i = N - 1 then
    decide (s < 3)
  else false

/--
The proposed valid-branch predicate separates the boundary unused branch that
caused the recorded `n = 3` collision, while the current executable map still
sends both branches to the same address.
-/
theorem robinSparseColumnBranchValid_boundaryUnused_n3 :
    robinSparseColumnBranchValid 3 0 0 = true ∧
      robinSparseColumnBranchValid 3 3 0 = false ∧
      robinSparseColumnMap 3 0 0 = robinSparseColumnMap 3 3 0 := by
  native_decide

/--
Proof-DAG block for the Lemma 1 address-range route.

For the fourth-order Robin stencil, if the input row is an `n`-bit value and
`n >= 2`, then the executable one-term column map also returns an `n`-bit
value.  The paper-level contract still records `addressRange.proved := false`
because the parameter-family side condition is not yet part of
`OneTermRobinParameters`.
-/
theorem robinSparseColumnMap_lt_gridSize_of_row_lt
    {n s i : Nat} (hn : 2 ≤ n) (hi : i < gridSize n) :
    robinSparseColumnMap n s i < gridSize n := by
  have hpow : 2 ^ 2 ≤ 2 ^ n :=
    Nat.pow_le_pow_right (by decide : 0 < 2) hn
  have hN4 : 4 ≤ gridSize n := by
    simpa [gridSize] using hpow
  unfold robinSparseColumnMap
  by_cases hbulk : 2 ≤ i ∧ i ≤ gridSize n - 3
  · simp [hbulk]
    by_cases hs : s < 5
    · simp [hs]
      omega
    · simp [hs, hi]
  · simp [hbulk]
    by_cases hi0 : i = 0
    · simp [hi0]
      by_cases hs : s < 3
      · simp [hs]
        omega
      · simp [hs]
        omega
    · simp [hi0]
      by_cases hi1 : i = 1
      · simp [hi1]
        by_cases hs : s < 4
        · simp [hs]
          omega
        · simp [hs]
          omega
      · simp [hi1]
        by_cases hiN2 : i = gridSize n - 2
        · simp [hiN2]
          by_cases hs : s < 4
          · simp [hs]
            omega
          · simp [hs]
            omega
        · simp [hiN2]
          by_cases hiN1 : i = gridSize n - 1
          · simp [hiN1]
            by_cases hs : s < 3
            · simp [hs]
              omega
            · simp [hs]
              omega
          · simp [hiN1, hi]

/--
Candidate reverse sparse index for the one-term Robin stencil.

Given a target row `target` and a post-SWAP row `row`, this returns the sparse
index that would make `row` address `target` in the executable fourth-order
Robin column map.  It is only a reverse-index candidate: the checked
roundtrip and cleanup obligations remain separate proof blocks.
Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478.
-/
def robinSparseReverseColumnIndex (n target row : Nat) : Nat :=
  let N := gridSize n
  if row = 0 then target
  else if row = 1 then target
  else if 2 ≤ row ∧ row ≤ N - 3 then target + 2 - row
  else if row = N - 2 then target - (N - 4)
  else if row = N - 1 then target - (N - 3)
  else target

/-- Normal form for the leftmost row of the executable Robin sparse map. -/
@[simp] theorem robinSparseColumnMap_zero (n s : Nat) :
    robinSparseColumnMap n s 0 = if s < 3 then s else 0 := by
  simp [robinSparseColumnMap]

/-- Normal form for the second row of the executable Robin sparse map. -/
@[simp] theorem robinSparseColumnMap_one (n s : Nat) :
    robinSparseColumnMap n s 1 = if s < 4 then s else 1 := by
  simp [robinSparseColumnMap]

/-- Normal form for a bulk row of the executable Robin sparse map. -/
theorem robinSparseColumnMap_bulk (n s i : Nat)
    (hbulk : 2 ≤ i ∧ i ≤ gridSize n - 3) :
    robinSparseColumnMap n s i = if s < 5 then i - 2 + s else i := by
  simp [robinSparseColumnMap, hbulk]

/-- Normal form for the penultimate row of the executable Robin sparse map. -/
theorem robinSparseColumnMap_rightBoundaryPrev {n s : Nat} (hn : 3 ≤ n) :
    robinSparseColumnMap n s (gridSize n - 2) =
      if s < 4 then gridSize n - 4 + s else gridSize n - 2 := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hnotbulk :
      ¬(2 ≤ gridSize n - 2 ∧ gridSize n ≤ gridSize n - 3 + 2) := by
    omega
  have hnot0 : gridSize n - 2 ≠ 0 := by omega
  have hnot1 : gridSize n - 2 ≠ 1 := by omega
  simp [robinSparseColumnMap, hnotbulk, hnot0, hnot1]

/-- Normal form for the last row of the executable Robin sparse map. -/
theorem robinSparseColumnMap_rightBoundaryLast {n s : Nat} (hn : 3 ≤ n) :
    robinSparseColumnMap n s (gridSize n - 1) =
      if s < 3 then gridSize n - 3 + s else gridSize n - 1 := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hnotbulk :
      ¬(2 ≤ gridSize n - 1 ∧ gridSize n ≤ gridSize n - 3 + 1) := by
    omega
  have hnot0 : gridSize n - 1 ≠ 0 := by omega
  have hnot1 : gridSize n - 1 ≠ 1 := by omega
  have hnotN2 : gridSize n - 1 ≠ gridSize n - 2 := by omega
  simp [robinSparseColumnMap, hnotbulk, hnot0, hnot1, hnotN2]

/-- Reverse-index normal form for row zero. -/
@[simp] theorem robinSparseReverseColumnIndex_zero (n target : Nat) :
    robinSparseReverseColumnIndex n target 0 = target := by
  simp [robinSparseReverseColumnIndex]

/-- Reverse-index normal form for row one. -/
@[simp] theorem robinSparseReverseColumnIndex_one (n target : Nat) :
    robinSparseReverseColumnIndex n target 1 = target := by
  simp [robinSparseReverseColumnIndex]

/-- Reverse-index normal form for a bulk row. -/
theorem robinSparseReverseColumnIndex_bulk (n target row : Nat)
    (hbulk : 2 ≤ row ∧ row ≤ gridSize n - 3) :
    robinSparseReverseColumnIndex n target row = target + 2 - row := by
  have hnot0 : row ≠ 0 := by omega
  have hnot1 : row ≠ 1 := by omega
  simp [robinSparseReverseColumnIndex, hbulk, hnot0, hnot1]

/-- Reverse-index normal form for the penultimate row. -/
theorem robinSparseReverseColumnIndex_rightBoundaryPrev
    {n target : Nat} (hn : 3 ≤ n) :
    robinSparseReverseColumnIndex n target (gridSize n - 2) =
      target - (gridSize n - 4) := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hnot0 : gridSize n - 2 ≠ 0 := by omega
  have hnot1 : gridSize n - 2 ≠ 1 := by omega
  have hnotbulk :
      ¬(2 ≤ gridSize n - 2 ∧ gridSize n ≤ gridSize n - 3 + 2) := by
    omega
  simp [robinSparseReverseColumnIndex, hnot0, hnot1, hnotbulk]

/-- Reverse-index normal form for the last row. -/
theorem robinSparseReverseColumnIndex_rightBoundaryLast
    {n target : Nat} (hn : 3 ≤ n) :
    robinSparseReverseColumnIndex n target (gridSize n - 1) =
      target - (gridSize n - 3) := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hnot0 : gridSize n - 1 ≠ 0 := by omega
  have hnot1 : gridSize n - 1 ≠ 1 := by omega
  have hnotbulk :
      ¬(2 ≤ gridSize n - 1 ∧ gridSize n ≤ gridSize n - 3 + 1) := by
    omega
  have hnotN2 : gridSize n - 1 ≠ gridSize n - 2 := by omega
  simp [robinSparseReverseColumnIndex, hnot0, hnot1, hnotbulk, hnotN2]

/--
The reverse sparse-index candidate is a left inverse for the executable
one-term Robin column map on the three-bit sparse-index range used by the
current one-term parameter family.

This is only the arithmetic roundtrip needed by the O_D^BS post-SWAP cleanup
route.  It does not prove uniqueness of the preimage, dagger cleanup, unitarity,
or block correctness.
-/
theorem robinSparseReverseColumnRoundtrip_of_lt_eight
    {n s i : Nat} (hn : 3 <= n) (hs : s < 8) (hi : i < gridSize n) :
    robinSparseColumnMap n
      (robinSparseReverseColumnIndex n i (robinSparseColumnMap n s i))
      (robinSparseColumnMap n s i) = i := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hs_cases : s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
      s = 4 ∨ s = 5 ∨ s = 6 ∨ s = 7 := by
    omega
  by_cases hi0 : i = 0
  · subst i
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex] <;>
      omega
  by_cases hi1 : i = 1
  · subst i
    have hbulk2 : 2 ≤ 2 ∧ 2 ≤ gridSize n - 3 := by omega
    have hbulk3 : 2 ≤ 3 ∧ 3 ≤ gridSize n - 3 := by omega
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex, hbulk2,
        hbulk3] <;>
      omega
  by_cases hiN2 : i = gridSize n - 2
  · subst i
    have hrowN4 : 2 ≤ gridSize n - 4 ∧ gridSize n - 4 ≤ gridSize n - 3 := by
      omega
    have hrowN3 : 2 ≤ gridSize n - 3 ∧ gridSize n - 3 ≤ gridSize n - 3 := by
      omega
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 0) hn]
      simp
      rw [robinSparseReverseColumnIndex_bulk n (gridSize n - 2)
        (gridSize n - 4) hrowN4]
      have hrev : gridSize n - 2 + 2 - (gridSize n - 4) = 4 := by omega
      rw [hrev, robinSparseColumnMap_bulk n 4 (gridSize n - 4) hrowN4]
      simp
      omega
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 1) hn]
      simp
      rw [show gridSize n - 4 + 1 = gridSize n - 3 by omega]
      rw [robinSparseReverseColumnIndex_bulk n (gridSize n - 2)
        (gridSize n - 3) hrowN3]
      have hrev : gridSize n - 2 + 2 - (gridSize n - 3) = 3 := by omega
      rw [hrev, robinSparseColumnMap_bulk n 3 (gridSize n - 3) hrowN3]
      simp
      omega
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 2) hn]
      simp
      rw [show gridSize n - 4 + 2 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 2) hn]
      have hrev : gridSize n - 2 - (gridSize n - 4) = 2 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 2) hn]
      simp
      omega
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 3) hn]
      simp
      rw [show gridSize n - 4 + 3 = gridSize n - 1 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 2) hn]
      have hrev : gridSize n - 2 - (gridSize n - 3) = 1 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryLast (n := n) (s := 1) hn]
      simp
      omega
    all_goals
      rw [robinSparseColumnMap_rightBoundaryPrev (n := n) hn]
      simp
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 2) hn]
      have hrev : gridSize n - 2 - (gridSize n - 4) = 2 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 2) hn]
      simp
      omega
  by_cases hiN1 : i = gridSize n - 1
  · subst i
    have hrowN3 : 2 ≤ gridSize n - 3 ∧ gridSize n - 3 ≤ gridSize n - 3 := by
      omega
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · rw [robinSparseColumnMap_rightBoundaryLast (n := n) (s := 0) hn]
      simp
      rw [robinSparseReverseColumnIndex_bulk n (gridSize n - 1)
        (gridSize n - 3) hrowN3]
      have hrev : gridSize n - 1 + 2 - (gridSize n - 3) = 4 := by omega
      rw [hrev, robinSparseColumnMap_bulk n 4 (gridSize n - 3) hrowN3]
      simp
      omega
    · rw [robinSparseColumnMap_rightBoundaryLast (n := n) (s := 1) hn]
      simp
      rw [show gridSize n - 3 + 1 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 1) hn]
      have hrev : gridSize n - 1 - (gridSize n - 4) = 3 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 3) hn]
      simp
      omega
    · rw [robinSparseColumnMap_rightBoundaryLast (n := n) (s := 2) hn]
      simp
      rw [show gridSize n - 3 + 2 = gridSize n - 1 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 1) hn]
      have hrev : gridSize n - 1 - (gridSize n - 3) = 2 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryLast (n := n) (s := 2) hn]
      simp
      omega
    all_goals
      rw [robinSparseColumnMap_rightBoundaryLast (n := n) hn]
      simp
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 1) hn]
      have hrev : gridSize n - 1 - (gridSize n - 3) = 2 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryLast (n := n) (s := 2) hn]
      simp
      omega
  have hbulk : 2 ≤ i ∧ i ≤ gridSize n - 3 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [robinSparseColumnMap_bulk n 0 i hbulk]
    simp
    by_cases hi2 : i = 2
    · subst i
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex]
    by_cases hi3 : i = 3
    · subst i
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex]
    have hrow : 2 ≤ i - 2 ∧ i - 2 ≤ gridSize n - 3 := by omega
    rw [robinSparseReverseColumnIndex_bulk n i (i - 2) hrow]
    have hrev : i + 2 - (i - 2) = 4 := by omega
    rw [hrev, robinSparseColumnMap_bulk n 4 (i - 2) hrow]
    simp
    omega
  · rw [robinSparseColumnMap_bulk n 1 i hbulk]
    simp
    by_cases hi2 : i = 2
    · subst i
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex]
    have hrow : 2 ≤ i - 1 ∧ i - 1 ≤ gridSize n - 3 := by omega
    rw [show i - 2 + 1 = i - 1 by omega]
    rw [robinSparseReverseColumnIndex_bulk n i (i - 1) hrow]
    have hrev : i + 2 - (i - 1) = 3 := by omega
    rw [hrev, robinSparseColumnMap_bulk n 3 (i - 1) hrow]
    simp
    omega
  · rw [robinSparseColumnMap_bulk n 2 i hbulk]
    simp
    rw [show i - 2 + 2 = i by omega]
    rw [robinSparseReverseColumnIndex_bulk n i i hbulk]
    have hrev : i + 2 - i = 2 := by omega
    rw [hrev, robinSparseColumnMap_bulk n 2 i hbulk]
    simp
    omega
  · rw [robinSparseColumnMap_bulk n 3 i hbulk]
    simp
    by_cases hiN3 : i = gridSize n - 3
    · subst i
      rw [show gridSize n - 3 - 2 + 3 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 3) hn]
      have hrev : gridSize n - 3 - (gridSize n - 4) = 1 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 1) hn]
      simp
      omega
    have hrow : 2 ≤ i - 2 + 3 ∧ i - 2 + 3 ≤ gridSize n - 3 := by
      omega
    rw [robinSparseReverseColumnIndex_bulk n i (i - 2 + 3) hrow]
    have hrev : i + 2 - (i - 2 + 3) = 1 := by omega
    rw [hrev, robinSparseColumnMap_bulk n 1 (i - 2 + 3) hrow]
    simp
    omega
  · rw [robinSparseColumnMap_bulk n 4 i hbulk]
    simp
    by_cases hiN3 : i = gridSize n - 3
    · subst i
      rw [show gridSize n - 3 - 2 + 4 = gridSize n - 1 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 3) hn]
      have hrev : gridSize n - 3 - (gridSize n - 3) = 0 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryLast (n := n) (s := 0) hn]
      simp
    by_cases hiN4 : i = gridSize n - 4
    · subst i
      rw [show gridSize n - 4 - 2 + 4 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 4) hn]
      have hrev : gridSize n - 4 - (gridSize n - 4) = 0 := by omega
      rw [hrev, robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 0) hn]
      simp
    have hrow : 2 ≤ i - 2 + 4 ∧ i - 2 + 4 ≤ gridSize n - 3 := by
      omega
    rw [robinSparseReverseColumnIndex_bulk n i (i - 2 + 4) hrow]
    have hrev : i + 2 - (i - 2 + 4) = 0 := by omega
    rw [hrev, robinSparseColumnMap_bulk n 0 (i - 2 + 4) hrow]
    simp
    omega
  all_goals
    rw [robinSparseColumnMap_bulk n _ i hbulk]
    simp
    rw [robinSparseReverseColumnIndex_bulk n i i hbulk]
    have hrev : i + 2 - i = 2 := by omega
    rw [hrev, robinSparseColumnMap_bulk n 2 i hbulk]
    simp
    omega

/--
The reverse-index candidate stays inside the three-bit sparse register for
columns produced by the executable one-term Robin map.

This is paired with `robinSparseReverseColumnRoundtrip_of_lt_eight`; it is a
local arithmetic block for the post-SWAP preimage route, not a uniqueness or
dagger-cleanup proof.
-/
theorem robinSparseReverseColumnIndex_lt_eight_of_columnMap
    {n s i : Nat} (hn : 3 <= n) (hs : s < 8) (hi : i < gridSize n) :
    robinSparseReverseColumnIndex n i (robinSparseColumnMap n s i) < 8 := by
  have hN8 : 8 ≤ gridSize n := by
    have hpow : 2 ^ 3 ≤ 2 ^ n :=
      Nat.pow_le_pow_right (by decide : 0 < 2) hn
    simpa [gridSize] using hpow
  have hs_cases : s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨
      s = 4 ∨ s = 5 ∨ s = 6 ∨ s = 7 := by
    omega
  by_cases hi0 : i = 0
  · subst i
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex] <;>
      omega
  by_cases hi1 : i = 1
  · subst i
    have hbulk2 : 2 ≤ 2 ∧ 2 ≤ gridSize n - 3 := by omega
    have hbulk3 : 2 ≤ 3 ∧ 3 ≤ gridSize n - 3 := by omega
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [robinSparseColumnMap, robinSparseReverseColumnIndex, hbulk2,
        hbulk3] <;>
      omega
  by_cases hiN2 : i = gridSize n - 2
  · subst i
    have hrowN4 : 2 ≤ gridSize n - 4 ∧ gridSize n - 4 ≤ gridSize n - 3 := by
      omega
    have hrowN3 : 2 ≤ gridSize n - 3 ∧ gridSize n - 3 ≤ gridSize n - 3 := by
      omega
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 0) hn]
      simp
      rw [robinSparseReverseColumnIndex_bulk n (gridSize n - 2)
        (gridSize n - 4) hrowN4]
      omega
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 1) hn]
      simp
      rw [show gridSize n - 4 + 1 = gridSize n - 3 by omega]
      rw [robinSparseReverseColumnIndex_bulk n (gridSize n - 2)
        (gridSize n - 3) hrowN3]
      omega
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 2) hn]
      simp
      rw [show gridSize n - 4 + 2 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 2) hn]
      omega
    · rw [robinSparseColumnMap_rightBoundaryPrev (n := n) (s := 3) hn]
      simp
      rw [show gridSize n - 4 + 3 = gridSize n - 1 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 2) hn]
      omega
    all_goals
      rw [robinSparseColumnMap_rightBoundaryPrev (n := n) hn]
      simp
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 2) hn]
      omega
  by_cases hiN1 : i = gridSize n - 1
  · subst i
    have hrowN3 : 2 ≤ gridSize n - 3 ∧ gridSize n - 3 ≤ gridSize n - 3 := by
      omega
    rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · rw [robinSparseColumnMap_rightBoundaryLast (n := n) (s := 0) hn]
      simp
      rw [robinSparseReverseColumnIndex_bulk n (gridSize n - 1)
        (gridSize n - 3) hrowN3]
      omega
    · rw [robinSparseColumnMap_rightBoundaryLast (n := n) (s := 1) hn]
      simp
      rw [show gridSize n - 3 + 1 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 1) hn]
      omega
    · rw [robinSparseColumnMap_rightBoundaryLast (n := n) (s := 2) hn]
      simp
      rw [show gridSize n - 3 + 2 = gridSize n - 1 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 1) hn]
      omega
    all_goals
      rw [robinSparseColumnMap_rightBoundaryLast (n := n) hn]
      simp
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 1) hn]
      omega
  have hbulk : 2 ≤ i ∧ i ≤ gridSize n - 3 := by
    omega
  rcases hs_cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [robinSparseColumnMap_bulk n 0 i hbulk]
    simp
    by_cases hi2 : i = 2
    · subst i
      simp [robinSparseReverseColumnIndex]
    by_cases hi3 : i = 3
    · subst i
      simp [robinSparseReverseColumnIndex]
    have hrow : 2 ≤ i - 2 ∧ i - 2 ≤ gridSize n - 3 := by omega
    rw [robinSparseReverseColumnIndex_bulk n i (i - 2) hrow]
    omega
  · rw [robinSparseColumnMap_bulk n 1 i hbulk]
    simp
    by_cases hi2 : i = 2
    · subst i
      simp [robinSparseReverseColumnIndex]
    have hrow : 2 ≤ i - 1 ∧ i - 1 ≤ gridSize n - 3 := by omega
    rw [show i - 2 + 1 = i - 1 by omega]
    rw [robinSparseReverseColumnIndex_bulk n i (i - 1) hrow]
    omega
  · rw [robinSparseColumnMap_bulk n 2 i hbulk]
    simp
    rw [show i - 2 + 2 = i by omega]
    rw [robinSparseReverseColumnIndex_bulk n i i hbulk]
    omega
  · rw [robinSparseColumnMap_bulk n 3 i hbulk]
    simp
    by_cases hiN3 : i = gridSize n - 3
    · subst i
      rw [show gridSize n - 3 - 2 + 3 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 3) hn]
      omega
    have hrow : 2 ≤ i - 2 + 3 ∧ i - 2 + 3 ≤ gridSize n - 3 := by
      omega
    rw [robinSparseReverseColumnIndex_bulk n i (i - 2 + 3) hrow]
    omega
  · rw [robinSparseColumnMap_bulk n 4 i hbulk]
    simp
    by_cases hiN3 : i = gridSize n - 3
    · subst i
      rw [show gridSize n - 3 - 2 + 4 = gridSize n - 1 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryLast
        (n := n) (target := gridSize n - 3) hn]
      omega
    by_cases hiN4 : i = gridSize n - 4
    · subst i
      rw [show gridSize n - 4 - 2 + 4 = gridSize n - 2 by omega]
      rw [robinSparseReverseColumnIndex_rightBoundaryPrev
        (n := n) (target := gridSize n - 4) hn]
      omega
    have hrow : 2 ≤ i - 2 + 4 ∧ i - 2 + 4 ≤ gridSize n - 3 := by
      omega
    rw [robinSparseReverseColumnIndex_bulk n i (i - 2 + 4) hrow]
    omega
  all_goals
    rw [robinSparseColumnMap_bulk n _ i hbulk]
    simp
    rw [robinSparseReverseColumnIndex_bulk n i i hbulk]
    omega

/--
Executable finite audit for the reverse-index candidate.

For each sparse-index value below `sparseBound` and each row of the `n`-qubit
grid, this checks that forward addressing followed by
`robinSparseReverseColumnIndex` returns to the original row.  A true result is
local evidence for the inverse-on-range route; it is not a semantic cleanup
proof for `O_D^BS`.
-/
def robinSparseReverseColumnRoundtripCheck (n sparseBound : Nat) : Bool :=
  (List.range sparseBound).all (fun s =>
    (List.range (gridSize n)).all (fun i =>
      robinSparseColumnMap n
          (robinSparseReverseColumnIndex n i (robinSparseColumnMap n s i))
          (robinSparseColumnMap n s i) == i))

/--
Register values used by the faithful Lemma 1 `O_D^BS` contract.

The current compound-index convention stores the row register in bits
`[1, 1+n)` and the paper's padded sparse-address register in bits
`[1+n, 1+2n)`.  Inside that address block, the low `n - clog2 kappa` bits are
the padded-zero workspace and the remaining bits encode the sparse index `s`.
Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478. -/
structure BandedSparseAccessPaperRegisters where
  odRegisterValue : Nat
  paddedZeroValue : Nat
  sparseIndexValue : Nat
  rowValue : Nat
deriving Repr, DecidableEq

/--
Extract the Lemma 1 padded sparse-address and row registers from a compound
basis index.  This is a source-contract skeleton only; it does not alter the
interim `bandedSparseAccessMatrix` helper and does not prove unitarity.
-/
def bandedSparseAccessPaperRegisters (p : OneTermRobinParameters) (j : Nat) :
    BandedSparseAccessPaperRegisters :=
  let n := p.n
  let κbits := clog2 p.kappa
  let odPure := n - κbits
  let nMask := (1 <<< n) - 1
  let zeroMask := (1 <<< odPure) - 1
  let sparseMask := (1 <<< κbits) - 1
  let odValue := (j >>> (1 + n)) &&& nMask
  {
    odRegisterValue := odValue
    paddedZeroValue := odValue &&& zeroMask
    sparseIndexValue := (odValue >>> odPure) &&& sparseMask
    rowValue := (j >>> 1) &&& nMask
  }

/-- The row field extracted for Lemma 1 is always an `n`-bit row value. -/
theorem bandedSparseAccessPaperRegisters_row_lt_gridSize
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p j).rowValue < gridSize p.n := by
  simp [bandedSparseAccessPaperRegisters, gridSize]
  rw [Nat.one_shiftLeft]
  apply Nat.and_lt_two_pow
  exact Nat.sub_lt (Nat.pow_pos (by decide : 0 < 2) : 0 < 2 ^ p.n) (by decide)

/-- The sparse-index field is the high sparse slice of the full O_D register. -/
theorem bandedSparseAccessPaperRegisters_sparseIndexValue_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p j).sparseIndexValue =
      (((bandedSparseAccessPaperRegisters p j).odRegisterValue >>>
          (p.n - clog2 p.kappa)) &&& ((1 <<< clog2 p.kappa) - 1)) := by
  rfl

/-- The padded-zero field is the low padded slice of the full O_D register. -/
theorem bandedSparseAccessPaperRegisters_paddedZeroValue_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p j).paddedZeroValue =
      ((bandedSparseAccessPaperRegisters p j).odRegisterValue &&&
        ((1 <<< (p.n - clog2 p.kappa)) - 1)) := by
  rfl

/-- The extracted sparse-index field always fits in its declared bit width. -/
theorem bandedSparseAccessPaperRegisters_sparseIndex_lt
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p j).sparseIndexValue <
      (1 <<< clog2 p.kappa) := by
  rw [bandedSparseAccessPaperRegisters_sparseIndexValue_eq]
  rw [Nat.one_shiftLeft]
  apply Nat.and_lt_two_pow
  exact Nat.sub_lt
    (Nat.pow_pos (by decide : 0 < 2) : 0 < 2 ^ clog2 p.kappa) (by decide)

/-- The extracted O_D register value always fits in its declared `n`-bit block. -/
theorem bandedSparseAccessPaperRegisters_odRegisterValue_lt
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p j).odRegisterValue < (1 <<< p.n) := by
  simp [bandedSparseAccessPaperRegisters]
  rw [Nat.one_shiftLeft]
  apply Nat.and_lt_two_pow
  exact Nat.sub_lt
    (Nat.pow_pos (by decide : 0 < 2) : 0 < 2 ^ p.n) (by decide)

/--
Rejected row-dependent paper-address helper.

This is the old active address model: it used `robinSparseColumnMap`, which
deletes boundary zero-amplitude sparse slots by folding them back to the row.
It is retained only for regression tests and proof-attempt memory.
-/
def bandedSparseAccessRowDependentPaperAddress
    (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let regs := bandedSparseAccessPaperRegisters p j
  robinSparseColumnMap p.n regs.sparseIndexValue regs.rowValue

/--
Paper address value `r_si` for the one-term Robin sparse-access oracle.

The active address follows the global sparse-slot formula
`r_si = r_s0 + i mod 2^n`.  Boundary or zero-amplitude slots remain present in
the sparse register; the coefficient layer supplies zero values where needed.
-/
def bandedSparseAccessPaperAddress (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let regs := bandedSparseAccessPaperRegisters p j
  oneTermRobinGlobalSparseAddress p.n regs.sparseIndexValue regs.rowValue

/-- Executable check that the paper address `r_si` fits in the n-bit address register. -/
def bandedSparseAccessPaperAddressInRange (p : OneTermRobinParameters) (j : Nat) : Bool :=
  decide (bandedSparseAccessPaperAddress p j < (1 <<< p.n))

/-- Boolean form of the executable `O_D^BS` address-range check. -/
theorem bandedSparseAccessPaperAddressInRange_iff
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperAddressInRange p j = true ↔
      bandedSparseAccessPaperAddress p j < (1 <<< p.n) := by
  unfold bandedSparseAccessPaperAddressInRange
  exact decide_eq_true_iff

/--
The executable paper address is in range for the fourth-order grid regime
`2 <= n`.  This is a reusable arithmetic block; it does not promote the
paper-level semantic obligation.
-/
theorem bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
    (p : OneTermRobinParameters) (j : Nat) (_hn : 2 ≤ p.n) :
    bandedSparseAccessPaperAddress p j < gridSize p.n := by
  unfold bandedSparseAccessPaperAddress
  exact oneTermRobinGlobalSparseAddress_lt_gridSize p.n
    (bandedSparseAccessPaperRegisters p j).sparseIndexValue
    (bandedSparseAccessPaperRegisters p j).rowValue

/--
The executable address-range Boolean evaluates to true for the fourth-order
grid regime `2 <= n`.  The contract flag remains false until the paper
parameter family records this side condition.
-/
theorem bandedSparseAccessPaperAddressInRange_eq_true_of_two_le
    (p : OneTermRobinParameters) (j : Nat) (hn : 2 ≤ p.n) :
    bandedSparseAccessPaperAddressInRange p j = true := by
  unfold bandedSparseAccessPaperAddressInRange
  have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le p j hn
  simpa [gridSize, Nat.one_shiftLeft] using h

/--
Executable Lemma 1 image skeleton for `O_D^BS`.

It preserves the row/system register and replaces the padded sparse-address
register by `r_si`.  Correctness, unitarity, and dagger cleanup remain recorded
in `defaultBandedSparseAccessPaperContract p` with `proved := false`.
-/
def bandedSparseAccessPaperImage (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  let highTail := j / highBase
  let address := bandedSparseAccessPaperAddress p j
  lowPrefix + address * lowBase + highTail * highBase

/--
Rejected row-dependent image helper corresponding to the old active address.

This has the same register splice as `bandedSparseAccessPaperImage`, but writes
the row-dependent helper address.  It is not the active paper image.
-/
def bandedSparseAccessRowDependentPaperImage
    (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  let highTail := j / highBase
  let address := bandedSparseAccessRowDependentPaperAddress p j
  lowPrefix + address * lowBase + highTail * highBase

/--
Bit-slice extraction as arithmetic division followed by an `n`-bit remainder.
This keeps later register-splice proofs in ordinary arithmetic form.
-/
theorem bandedSparseAccessPaperRegisterValue_eq_mod
    (x offset n : Nat) :
    ((x >>> offset) &&& ((1 <<< n) - 1)) =
      (x / 2 ^ offset) % 2 ^ n := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp only [Nat.testBit_and, Nat.testBit_shiftRight, Nat.one_shiftLeft,
    Nat.testBit_two_pow_sub_one, Nat.testBit_mod_two_pow]
  by_cases hi : i < n
  · simp [hi]
    rw [Nat.add_comm offset i, Nat.testBit_add]
  · simp [hi]

/-- The O_D^BS address block ends before the full one-term Robin basis width. -/
theorem bandedSparseAccessPaperHighWidth_le_totalQubits
    (p : OneTermRobinParameters) :
    1 + 2 * p.n ≤ oneTermRobinTotalQubits p := by
  simp only [oneTermRobinTotalQubits, RobinRegisterPartition.totalQubits,
    defaultRobinRegisterPartition]
  omega

/--
The low block of the paper image fits below the high-tail boundary whenever the
written O_D^BS address is an n-bit value.
-/
theorem bandedSparseAccessPaperImage_lowBlock_lt_highBase_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    let lowWidth := 1 + p.n
    let highWidth := 1 + 2 * p.n
    let lowBase := 2 ^ lowWidth
    let highBase := 2 ^ highWidth
    let lowPrefix := j % lowBase
    let address := bandedSparseAccessPaperAddress p j
    lowPrefix + address * lowBase < highBase := by
  rw [Nat.one_shiftLeft] at haddr
  dsimp
  have hlowPos : 0 < 2 ^ (1 + p.n) :=
    Nat.pow_pos (by decide : 0 < 2)
  have hlow : j % 2 ^ (1 + p.n) < 2 ^ (1 + p.n) :=
    Nat.mod_lt j hlowPos
  have hbase : 2 ^ (1 + 2 * p.n) = 2 ^ (1 + p.n) * 2 ^ p.n := by
    rw [← Nat.pow_add]
    congr 1
    omega
  rw [hbase]
  have hlt1 :
      j % 2 ^ (1 + p.n) +
          bandedSparseAccessPaperAddress p j * 2 ^ (1 + p.n) <
        2 ^ (1 + p.n) +
          bandedSparseAccessPaperAddress p j * 2 ^ (1 + p.n) := by
    exact Nat.add_lt_add_right hlow
      (bandedSparseAccessPaperAddress p j * 2 ^ (1 + p.n))
  have hsucc : bandedSparseAccessPaperAddress p j + 1 ≤ 2 ^ p.n :=
    Nat.succ_le_of_lt haddr
  have hle :
      (bandedSparseAccessPaperAddress p j + 1) * 2 ^ (1 + p.n) ≤
        2 ^ p.n * 2 ^ (1 + p.n) := by
    exact Nat.mul_le_mul_right (2 ^ (1 + p.n)) hsucc
  have heq :
      2 ^ (1 + p.n) +
          bandedSparseAccessPaperAddress p j * 2 ^ (1 + p.n) =
        (bandedSparseAccessPaperAddress p j + 1) * 2 ^ (1 + p.n) := by
    rw [Nat.add_comm]
    exact (Nat.succ_mul (bandedSparseAccessPaperAddress p j)
      (2 ^ (1 + p.n))).symm
  rw [heq] at hlt1
  rw [Nat.mul_comm (2 ^ (1 + p.n)) (2 ^ p.n)]
  exact Nat.lt_of_lt_of_le hlt1 hle

/-- The paper image preserves the low ancilla-and-row block modulo its width. -/
theorem bandedSparseAccessPaperImage_mod_lowBase
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperImage p j % 2 ^ (1 + p.n) =
      j % 2 ^ (1 + p.n) := by
  unfold bandedSparseAccessPaperImage
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  let highTail := j / highBase
  let address := bandedSparseAccessPaperAddress p j
  have hbase : highBase = lowBase * 2 ^ p.n := by
    dsimp [highBase, lowBase, highWidth, lowWidth]
    rw [← Nat.pow_add]
    congr 1
    omega
  have hlow : lowPrefix % lowBase = lowPrefix := by
    dsimp [lowPrefix]
    exact Nat.mod_eq_of_lt (Nat.mod_lt j (Nat.pow_pos (by decide : 0 < 2)))
  calc
    (lowPrefix + address * lowBase + highTail * highBase) % lowBase
        = (lowPrefix + lowBase * address + highTail * highBase) % lowBase := by
          rw [Nat.mul_comm address lowBase]
    _ = (lowPrefix + lowBase * address + highTail * (lowBase * 2 ^ p.n)) % lowBase := by
          rw [hbase]
    _ = (lowPrefix + lowBase * (address + highTail * 2 ^ p.n)) % lowBase := by
          congr 1
          rw [Nat.mul_add]
          ac_rfl
    _ = lowPrefix % lowBase := by
          rw [Nat.add_mul_mod_self_left]
    _ = lowPrefix := hlow
    _ = j % 2 ^ (1 + p.n) := by rfl

/--
After shifting past the low block, the paper image exposes the written address
modulo the n-bit O_D^BS register.
-/
theorem bandedSparseAccessPaperImage_div_lowBase_mod_eq
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    bandedSparseAccessPaperImage p j / 2 ^ (1 + p.n) % 2 ^ p.n =
      bandedSparseAccessPaperAddress p j := by
  unfold bandedSparseAccessPaperImage
  rw [Nat.one_shiftLeft] at haddr
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  let highTail := j / highBase
  let address := bandedSparseAccessPaperAddress p j
  have hlowPos : 0 < lowBase := by
    dsimp [lowBase, lowWidth]
    exact Nat.pow_pos (by decide : 0 < 2)
  have hlow : lowPrefix < lowBase := by
    dsimp [lowPrefix]
    exact Nat.mod_lt j hlowPos
  have hbase : highBase = lowBase * 2 ^ p.n := by
    dsimp [highBase, lowBase, highWidth, lowWidth]
    rw [← Nat.pow_add]
    congr 1
    omega
  have himage : lowPrefix + address * lowBase + highTail * highBase =
      lowPrefix + lowBase * (address + highTail * 2 ^ p.n) := by
    rw [hbase]
    rw [Nat.mul_add]
    ac_rfl
  have hdiv :
      (lowPrefix + lowBase * (address + highTail * 2 ^ p.n)) / lowBase =
        address + highTail * 2 ^ p.n := by
    rw [Nat.add_mul_div_left _ _ hlowPos]
    rw [Nat.div_eq_of_lt hlow]
    simp
  have hlowWidth : 2 ^ (1 + p.n) = lowBase := by rfl
  rw [hlowWidth]
  rw [himage]
  rw [hdiv]
  rw [Nat.add_mul_mod_self_right]
  exact Nat.mod_eq_of_lt haddr

/--
The executable paper image remains inside the full finite basis when the input
column is in range and the written O_D^BS address is n-bit.
-/
theorem bandedSparseAccessPaperImage_lt_qubitDim_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (hj : j < qubitDim (oneTermRobinTotalQubits p))
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    bandedSparseAccessPaperImage p j < qubitDim (oneTermRobinTotalQubits p) := by
  simp only [qubitDim, gridSize] at hj ⊢
  unfold bandedSparseAccessPaperImage
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  let highTail := j / highBase
  let address := bandedSparseAccessPaperAddress p j
  have hsmall :
      lowPrefix + address * lowBase < highBase :=
    bandedSparseAccessPaperImage_lowBlock_lt_highBase_of_address_lt p j haddr
  have hwidth : highWidth ≤ oneTermRobinTotalQubits p := by
    dsimp [highWidth]
    exact bandedSparseAccessPaperHighWidth_le_totalQubits p
  have hpowTotal : highBase * 2 ^ (oneTermRobinTotalQubits p - highWidth) =
      2 ^ oneTermRobinTotalQubits p := by
    dsimp [highBase]
    rw [← Nat.pow_add]
    congr 1
    omega
  have htail_lt : highTail < 2 ^ (oneTermRobinTotalQubits p - highWidth) := by
    dsimp [highTail]
    apply Nat.div_lt_of_lt_mul
    rwa [hpowTotal]
  have htail_succ : highTail + 1 ≤ 2 ^ (oneTermRobinTotalQubits p - highWidth) :=
    Nat.succ_le_of_lt htail_lt
  have hblock :
      lowPrefix + address * lowBase + highTail * highBase <
        highBase * (highTail + 1) := by
    rw [Nat.mul_succ, Nat.mul_comm highBase highTail]
    omega
  have htotal : highBase * (highTail + 1) ≤ 2 ^ oneTermRobinTotalQubits p := by
    have hmul := Nat.mul_le_mul_left highBase htail_succ
    rwa [hpowTotal] at hmul
  exact Nat.lt_of_lt_of_le hblock htotal

/--
Finite-basis index for the executable Lemma 1 `O_D^BS` paper image.

This constructor is available only when the source column is already in the
full finite basis and the written `O_D^BS` address is n-bit.  It is a bridge
from the arithmetic image function to matrix entries, not a unitarity proof.
-/
def bandedSparseAccessPaperImageFin
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    Fin (qubitDim (oneTermRobinTotalQubits p)) :=
  ⟨bandedSparseAccessPaperImage p j.val,
    bandedSparseAccessPaperImage_lt_qubitDim_of_address_lt p j.val j.2 haddr⟩

@[simp] theorem bandedSparseAccessPaperImageFin_val
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    (bandedSparseAccessPaperImageFin p j haddr).val =
      bandedSparseAccessPaperImage p j.val := rfl

/-- Register extraction from the paper image preserves the row register. -/
theorem bandedSparseAccessPaperImage_rowValue_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p
      (bandedSparseAccessPaperImage p j)).rowValue =
      (bandedSparseAccessPaperRegisters p j).rowValue := by
  unfold bandedSparseAccessPaperRegisters
  simp only []
  rw [bandedSparseAccessPaperRegisterValue_eq_mod,
    bandedSparseAccessPaperRegisterValue_eq_mod]
  have hpow : 2 * 2 ^ p.n = 2 ^ (1 + p.n) := by
    rw [show 1 + p.n = p.n + 1 by omega, Nat.pow_succ]
    omega
  have hmod := bandedSparseAccessPaperImage_mod_lowBase p j
  rw [← hpow] at hmod
  rw [← Nat.mod_mul_right_div_self (bandedSparseAccessPaperImage p j) 2 (2 ^ p.n)]
  rw [← Nat.mod_mul_right_div_self j 2 (2 ^ p.n)]
  rw [hmod]

/-- Register extraction from the paper image reports the written O_D^BS address. -/
theorem bandedSparseAccessPaperImage_odRegisterValue_eq
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    (bandedSparseAccessPaperRegisters p
      (bandedSparseAccessPaperImage p j)).odRegisterValue =
      bandedSparseAccessPaperAddress p j := by
  unfold bandedSparseAccessPaperRegisters
  simp only []
  rw [bandedSparseAccessPaperRegisterValue_eq_mod]
  exact bandedSparseAccessPaperImage_div_lowBase_mod_eq p j haddr

/-- High signal/workspace bits above the n-bit `O_D^BS` address register. -/
def bandedSparseAccessPaperHighTail (p : OneTermRobinParameters) (j : Nat) : Nat :=
  j >>> (1 + 2 * p.n)

/--
The arithmetic register-splice form of `bandedSparseAccessPaperImage` preserves
all bits above the `O_D^BS` address register when the written address is n-bit.

This is a proof-DAG block for Lemma 1 register safety.  It does not promote the
paper-level `noSpill` obligation because the parameter-family side conditions
are still tracked by `defaultBandedSparseAccessPaperContract`.
-/
theorem bandedSparseAccessPaperImage_highTail_eq_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    bandedSparseAccessPaperHighTail p (bandedSparseAccessPaperImage p j) =
      bandedSparseAccessPaperHighTail p j := by
  unfold bandedSparseAccessPaperHighTail
  rw [Nat.shiftRight_eq_div_pow, Nat.shiftRight_eq_div_pow]
  unfold bandedSparseAccessPaperImage
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  let highTail := j / highBase
  let address := bandedSparseAccessPaperAddress p j
  have hhighPos : 0 < highBase := by
    dsimp [highBase, highWidth]
    exact Nat.pow_pos (by decide : 0 < 2)
  have hsmall : lowPrefix + address * lowBase < highBase :=
    bandedSparseAccessPaperImage_lowBlock_lt_highBase_of_address_lt p j haddr
  have hdivsmall : (lowPrefix + address * lowBase) / highBase = 0 :=
    Nat.div_eq_of_lt hsmall
  calc
    (lowPrefix + address * lowBase + highTail * highBase) / highBase
        = (lowPrefix + address * lowBase + highBase * highTail) / highBase := by
          rw [Nat.mul_comm highTail highBase]
    _ = (lowPrefix + address * lowBase) / highBase + highTail := by
          rw [Nat.add_mul_div_left _ _ hhighPos]
    _ = highTail := by simp [hdivsmall]
    _ = j / highBase := rfl

/--
Executable check that the paper-image skeleton does not write past the n-bit
`O_D^BS` address register into the indicator or `m_f` bits above it.
-/
def bandedSparseAccessPaperImageNoSpill (p : OneTermRobinParameters) (j : Nat) : Bool :=
  bandedSparseAccessPaperHighTail p (bandedSparseAccessPaperImage p j) ==
    bandedSparseAccessPaperHighTail p j

/--
Boolean form of the executable high-tail no-spill check.

The high-tail theorem above discharges this Boolean under an n-bit written
address, while the paper-level semantic obligation remains a separate flag.
-/
theorem bandedSparseAccessPaperImageNoSpill_iff
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperImageNoSpill p j = true ↔
      bandedSparseAccessPaperHighTail p (bandedSparseAccessPaperImage p j) =
        bandedSparseAccessPaperHighTail p j := by
  unfold bandedSparseAccessPaperImageNoSpill
  exact beq_iff_eq

/-- The no-spill Boolean follows from the executable n-bit address bound. -/
theorem bandedSparseAccessPaperImageNoSpill_eq_true_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    bandedSparseAccessPaperImageNoSpill p j = true := by
  rw [bandedSparseAccessPaperImageNoSpill_iff]
  exact bandedSparseAccessPaperImage_highTail_eq_of_address_lt p j haddr

/--
The no-spill Boolean is true in the fourth-order grid regime `2 <= n`, reusing
the address-range proof-DAG block.  Semantic obligation flags remain false.
-/
theorem bandedSparseAccessPaperImageNoSpill_eq_true_of_two_le
    (p : OneTermRobinParameters) (j : Nat) (hn : 2 ≤ p.n) :
    bandedSparseAccessPaperImageNoSpill p j = true := by
  apply bandedSparseAccessPaperImageNoSpill_eq_true_of_address_lt
  have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le p j hn
  simpa [gridSize, Nat.one_shiftLeft] using h

/--
Clean-domain predicate for the Lemma 1 `O_D^BS` source equation.

The paper specifies columns whose padded zero register is `|0>^(n-l)`.
Columns outside this domain still need a separate unitary-completion proof;
the current paper-image matrix is only a Phase 1 skeleton for that full-space
extension.
-/
def bandedSparseAccessPaperCleanInput (p : OneTermRobinParameters) (j : Nat) : Bool :=
  (bandedSparseAccessPaperRegisters p j).paddedZeroValue == 0

/--
Faithful sparse-slot range for the Lemma 1 `O_D^BS` source equation.

The paper source domain keeps the global slot `s` whenever `s < kappa`.
Whether a boundary coefficient is zero is handled by the amplitude layer, not
by deleting the sparse-register slot from the index oracle.
-/
def bandedSparseAccessPaperSparseIndexInKappa
    (p : OneTermRobinParameters) (j : Nat) : Bool :=
  decide ((bandedSparseAccessPaperRegisters p j).sparseIndexValue < p.kappa)

/--
Faithful clean source domain for the active global-slot `O_D^BS` address.

This predicate is the padded clean input from Lemma 1 together with the global
slot range `s < kappa`.  It supersedes the row-dependent nonzero-branch
classifier as the active source-domain contract for `bandedSparseAccessPaperImage`.
-/
def bandedSparseAccessPaperGlobalSlotSource
    (p : OneTermRobinParameters) (j : Nat) : Bool :=
  bandedSparseAccessPaperCleanInput p j &&
    bandedSparseAccessPaperSparseIndexInKappa p j

/-- A faithful global-slot source column is clean in the padded O_D register. -/
theorem bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperGlobalSlotSource p j = true) :
    bandedSparseAccessPaperCleanInput p j = true := by
  cases hclean : bandedSparseAccessPaperCleanInput p j <;>
    cases hinRange : bandedSparseAccessPaperSparseIndexInKappa p j <;>
    simp [bandedSparseAccessPaperGlobalSlotSource, hclean, hinRange] at h ⊢

/-- A faithful global-slot source column has sparse index below `kappa`. -/
theorem bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperGlobalSlotSource p j = true) :
    (bandedSparseAccessPaperRegisters p j).sparseIndexValue < p.kappa := by
  have hinRangeTrue :
      bandedSparseAccessPaperSparseIndexInKappa p j = true := by
    cases hclean : bandedSparseAccessPaperCleanInput p j <;>
      cases hinRange : bandedSparseAccessPaperSparseIndexInKappa p j <;>
      simp [bandedSparseAccessPaperGlobalSlotSource, hclean, hinRange] at h ⊢
  simpa [bandedSparseAccessPaperSparseIndexInKappa] using hinRangeTrue

/--
Global-source wrapper for inverse-slot injectivity.

For the one-term Robin `κ = 7` family, two active global-source columns with
the same reverse sparse slot have the same extracted sparse slot.  This is a
local source-domain block for the later unique-preimage proof; it does not
promote inverse-on-range, cleanup, or unitarity obligations.
-/
theorem bandedSparseAccessPaperGlobalSlotSource_inverseSlot_injective
    (p : OneTermRobinParameters) {j₁ j₂ : Nat}
    (hkappa : p.kappa = 7)
    (hsource₁ : bandedSparseAccessPaperGlobalSlotSource p j₁ = true)
    (hsource₂ : bandedSparseAccessPaperGlobalSlotSource p j₂ = true)
    (h :
      oneTermRobinGlobalSparseInverseSlot
          (bandedSparseAccessPaperRegisters p j₁).sparseIndexValue =
        oneTermRobinGlobalSparseInverseSlot
          (bandedSparseAccessPaperRegisters p j₂).sparseIndexValue) :
    (bandedSparseAccessPaperRegisters p j₁).sparseIndexValue =
      (bandedSparseAccessPaperRegisters p j₂).sparseIndexValue := by
  apply oneTermRobinGlobalSparseInverseSlot_injective_of_lt_seven
  · have hs :=
      bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
        p j₁ hsource₁
    rwa [hkappa] at hs
  · have hs :=
      bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
      p j₂ hsource₂
    rwa [hkappa] at hs
  · exact h

/--
Same-row injectivity of the active paper address on the global-slot source
domain.

This lifts the seven-slot address lemma through the Lemma 1 register extractor:
if two active global-source columns have the same row and the same corrected
paper address, then their sparse slots are equal.  It does not assert matrix
unitarity or dagger cleanup.
-/
theorem bandedSparseAccessPaperAddress_same_row_injective_of_globalSlotSource
    (p : OneTermRobinParameters) {j₁ j₂ : Nat}
    (hn : 3 ≤ p.n) (hkappa : p.kappa = 7)
    (hsource₁ : bandedSparseAccessPaperGlobalSlotSource p j₁ = true)
    (hsource₂ : bandedSparseAccessPaperGlobalSlotSource p j₂ = true)
    (hrow :
      (bandedSparseAccessPaperRegisters p j₁).rowValue =
        (bandedSparseAccessPaperRegisters p j₂).rowValue)
    (haddr :
      bandedSparseAccessPaperAddress p j₁ =
        bandedSparseAccessPaperAddress p j₂) :
    (bandedSparseAccessPaperRegisters p j₁).sparseIndexValue =
      (bandedSparseAccessPaperRegisters p j₂).sparseIndexValue := by
  have hs₁ :
      (bandedSparseAccessPaperRegisters p j₁).sparseIndexValue < 7 := by
    have hs :=
      bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
        p j₁ hsource₁
    rwa [hkappa] at hs
  have hs₂ :
      (bandedSparseAccessPaperRegisters p j₂).sparseIndexValue < 7 := by
    have hs :=
      bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
        p j₂ hsource₂
    rwa [hkappa] at hs
  have hrowLt :
      (bandedSparseAccessPaperRegisters p j₁).rowValue < gridSize p.n :=
    bandedSparseAccessPaperRegisters_row_lt_gridSize p j₁
  have haddrSame :
      oneTermRobinGlobalSparseAddress p.n
          (bandedSparseAccessPaperRegisters p j₁).sparseIndexValue
          (bandedSparseAccessPaperRegisters p j₁).rowValue =
        oneTermRobinGlobalSparseAddress p.n
          (bandedSparseAccessPaperRegisters p j₂).sparseIndexValue
          (bandedSparseAccessPaperRegisters p j₁).rowValue := by
    simpa [bandedSparseAccessPaperAddress, hrow] using haddr
  exact oneTermRobinGlobalSparseAddress_same_row_injective_of_lt_seven
    hn hs₁ hs₂ hrowLt haddrSame

/--
Candidate row-dependent sparse-branch domain for a basis column of Lemma 1.

This is deliberately separate from `bandedSparseAccessPaperCleanInput`.  The
paper clean-input condition only checks the padded zero register, while this
candidate also excludes row-boundary sparse indices that do not correspond to
nonzero stencil entries.  It is now a rejected-model audit helper; the active
paper source domain is `bandedSparseAccessPaperGlobalSlotSource`.
-/
def bandedSparseAccessPaperValidSparseBranch
    (p : OneTermRobinParameters) (j : Nat) : Bool :=
  let regs := bandedSparseAccessPaperRegisters p j
  robinSparseColumnBranchValid p.n regs.sparseIndexValue regs.rowValue

/--
Candidate corrected clean source domain for Lemma 1: padded-zero input plus a
row-dependent valid sparse branch.  This is a rejected-model contract-audit
predicate only.  Use `bandedSparseAccessPaperGlobalSlotSource` for the active
global-slot source contract.
-/
def bandedSparseAccessPaperValidCleanSource
    (p : OneTermRobinParameters) (j : Nat) : Bool :=
  bandedSparseAccessPaperCleanInput p j &&
    bandedSparseAccessPaperValidSparseBranch p j

/-- The corrected source-domain candidate implies the original clean input. -/
theorem bandedSparseAccessPaperValidCleanSource_cleanInput_eq_true
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperValidCleanSource p j = true) :
    bandedSparseAccessPaperCleanInput p j = true := by
  cases hclean : bandedSparseAccessPaperCleanInput p j <;>
    cases hvalid : bandedSparseAccessPaperValidSparseBranch p j <;>
    simp [bandedSparseAccessPaperValidCleanSource, hclean, hvalid] at h ⊢

/-- The corrected source-domain candidate implies a valid sparse branch. -/
theorem bandedSparseAccessPaperValidCleanSource_validSparseBranch_eq_true
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperValidCleanSource p j = true) :
    bandedSparseAccessPaperValidSparseBranch p j = true := by
  cases hclean : bandedSparseAccessPaperCleanInput p j <;>
    cases hvalid : bandedSparseAccessPaperValidSparseBranch p j <;>
    simp [bandedSparseAccessPaperValidCleanSource, hclean, hvalid] at h ⊢

/--
The row-dependent valid-source audit excludes the concrete unused sparse
branch from the recorded `n = 3`, `kappa = 7` rejected-model collision.  The
active global-slot paper image now separates the same two clean columns.
-/
theorem bandedSparseAccessPaperValidCleanSource_separates_boundaryCollision_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperCleanInput p 0 = true ∧
      bandedSparseAccessPaperCleanInput p 48 = true ∧
      bandedSparseAccessPaperValidSparseBranch p 0 = true ∧
      bandedSparseAccessPaperValidSparseBranch p 48 = false ∧
      bandedSparseAccessPaperValidCleanSource p 0 = true ∧
      bandedSparseAccessPaperValidCleanSource p 48 = false ∧
      bandedSparseAccessRowDependentPaperImage p 0 =
        bandedSparseAccessRowDependentPaperImage p 48 ∧
      bandedSparseAccessPaperImage p 0 ≠ bandedSparseAccessPaperImage p 48 := by
  native_decide

/--
Classifier for clean padded-register columns whose sparse branch is invalid
for the row-dependent Robin stencil.

This is the source-domain side of the unused-branch extension obligation.  The
active O_D^BS matrices are not changed by this predicate.
-/
def bandedSparseAccessPaperUnusedSparseBranch
    (p : OneTermRobinParameters) (j : Nat) : Bool :=
  bandedSparseAccessPaperCleanInput p j &&
    !bandedSparseAccessPaperValidSparseBranch p j

/-- An unused sparse branch is still in the padded clean-input domain. -/
theorem bandedSparseAccessPaperUnusedSparseBranch_cleanInput_eq_true
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperUnusedSparseBranch p j = true) :
    bandedSparseAccessPaperCleanInput p j = true := by
  cases hclean : bandedSparseAccessPaperCleanInput p j <;>
    cases hvalid : bandedSparseAccessPaperValidSparseBranch p j <;>
    simp [bandedSparseAccessPaperUnusedSparseBranch, hclean, hvalid] at h ⊢

/-- An unused sparse branch is outside the row-dependent valid-branch classifier. -/
theorem bandedSparseAccessPaperUnusedSparseBranch_validSparseBranch_eq_false
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperUnusedSparseBranch p j = true) :
    bandedSparseAccessPaperValidSparseBranch p j = false := by
  cases hclean : bandedSparseAccessPaperCleanInput p j <;>
    cases hvalid : bandedSparseAccessPaperValidSparseBranch p j <;>
    simp [bandedSparseAccessPaperUnusedSparseBranch, hclean, hvalid] at h ⊢

/--
The executable clean padded-input domain splits into valid sparse branches and
clean unused sparse branches.

This is only the local Boolean classifier split for the source-contract audit.
It does not choose an image for unused branches and does not promote the
semantic `cleanDomainSplit` obligation in the full-domain wrapper.
-/
theorem bandedSparseAccessPaperCleanDomainSplit_iff
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperCleanInput p j = true ↔
      bandedSparseAccessPaperValidCleanSource p j = true ∨
        bandedSparseAccessPaperUnusedSparseBranch p j = true := by
  constructor
  · intro hclean
    cases hvalid : bandedSparseAccessPaperValidSparseBranch p j <;>
      simp [bandedSparseAccessPaperValidCleanSource,
        bandedSparseAccessPaperUnusedSparseBranch, hclean, hvalid]
  · intro hsplit
    rcases hsplit with hvalidClean | hunused
    · exact
        bandedSparseAccessPaperValidCleanSource_cleanInput_eq_true
          p j hvalidClean
    · exact
        bandedSparseAccessPaperUnusedSparseBranch_cleanInput_eq_true
          p j hunused

/--
The two branches in `bandedSparseAccessPaperCleanDomainSplit_iff` are disjoint.

This is a classifier fact only; injectivity and unitary extension for the
eventual image rule remain separate false obligations.
-/
theorem bandedSparseAccessPaperCleanDomainSplit_disjoint
    (p : OneTermRobinParameters) (j : Nat) :
    ¬ (bandedSparseAccessPaperValidCleanSource p j = true ∧
        bandedSparseAccessPaperUnusedSparseBranch p j = true) := by
  intro hboth
  have hvalid :
      bandedSparseAccessPaperValidSparseBranch p j = true :=
    bandedSparseAccessPaperValidCleanSource_validSparseBranch_eq_true
      p j hboth.1
  have hinvalid :
      bandedSparseAccessPaperValidSparseBranch p j = false :=
    bandedSparseAccessPaperUnusedSparseBranch_validSparseBranch_eq_false
      p j hboth.2
  rw [hvalid] at hinvalid
  contradiction

/--
Interface for the missing reversible image rule on clean unused sparse branches.

No paper-backed formula has been selected yet, so `proposedImageIndex` is
`none` and every semantic claim remains an explicit false obligation.  The
active `bandedSparseAccessPaperImage` skeleton is not changed by this record.
-/
structure BandedSparseAccessUnusedBranchImageRuleContract where
  sourceAnchor : String
  sourceIndex : Nat
  inputRegisters : BandedSparseAccessPaperRegisters
  activeImageIndex : Nat
  proposedImageIndex : Option Nat
  cleanInput : Bool
  validSparseBranch : Bool
  unusedSparseBranch : Bool
  imageSpecified : ObligationRecord
  imageFinite : ObligationRecord
  separatesActiveCollision : ObligationRecord
  validBranchAgreement : ObligationRecord
deriving Repr, DecidableEq

/--
Default image-rule interface for one unused-branch source column.

The missing reversible image is intentionally represented by `none`; later
faithful work must replace this with a paper-compatible extension before any
injectivity, dagger-cleanup, or unitarity proof is attempted.
-/
def bandedSparseAccessUnusedBranchImageRuleContract
    (p : OneTermRobinParameters) (j : Nat) :
    BandedSparseAccessUnusedBranchImageRuleContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1 and one-term Robin zero-branch audit, arXiv:2506.20478"
  sourceIndex := j
  inputRegisters := bandedSparseAccessPaperRegisters p j
  activeImageIndex := bandedSparseAccessPaperImage p j
  proposedImageIndex := none
  cleanInput := bandedSparseAccessPaperCleanInput p j
  validSparseBranch := bandedSparseAccessPaperValidSparseBranch p j
  unusedSparseBranch := bandedSparseAccessPaperUnusedSparseBranch p j
  imageSpecified := {
    description := "a faithful reversible image for this clean invalid sparse branch is specified separately from the active colliding image"
    source := "QBE-AUTO-002 O_D^BS unused-branch image-rule interface"
    proved := false
  }
  imageFinite := {
    description := "the specified unused-branch image is a finite basis index in the one-term Robin Hilbert space"
    source := "QBE-AUTO-002 O_D^BS unused-branch image-rule interface"
    proved := false
  }
  separatesActiveCollision := {
    description := "the specified unused-branch image separates the known active-image collision on clean invalid branches"
    source := "QBE-AUTO-002 O_D^BS unused-branch image-rule interface"
    proved := false
  }
  validBranchAgreement := {
    description := "the eventual extension agrees with the Lemma 1 paper image on valid clean sparse branches"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- The unused-branch image-rule interface is obligation-only in Phase 1. -/
theorem bandedSparseAccessUnusedBranchImageRuleContract_flags_false
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessUnusedBranchImageRuleContract p j).proposedImageIndex = none ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).imageSpecified.proved = false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).imageFinite.proved = false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).separatesActiveCollision.proved = false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).validBranchAgreement.proved = false := by
  simp [bandedSparseAccessUnusedBranchImageRuleContract]

/--
Classifier bridge for the unused-branch image-rule interface.

For a clean invalid sparse branch, Lean records the branch classification and
keeps the image-rule target unspecified with false proof fields.
-/
theorem bandedSparseAccessUnusedBranchImageRuleContract_of_unusedBranch
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperUnusedSparseBranch p j = true) :
    (bandedSparseAccessUnusedBranchImageRuleContract p j).cleanInput = true ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).validSparseBranch = false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).unusedSparseBranch = true ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).proposedImageIndex = none ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).imageSpecified.proved = false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).validBranchAgreement.proved = false := by
  have hclean :
      bandedSparseAccessPaperCleanInput p j = true :=
    bandedSparseAccessPaperUnusedSparseBranch_cleanInput_eq_true p j h
  have hvalid :
      bandedSparseAccessPaperValidSparseBranch p j = false :=
    bandedSparseAccessPaperUnusedSparseBranch_validSparseBranch_eq_false p j h
  simp [bandedSparseAccessUnusedBranchImageRuleContract, h, hclean, hvalid]

/--
Contract slot for a faithful reversible extension on unused sparse branches.

GHL2025 keeps zero-amplitude sparse branches inside the kappa-wide register.
The current active image skeleton can collide on such branches, so Phase 1
records the missing extension as obligations instead of proving injectivity or
unitarity for the colliding skeleton.
-/
structure BandedSparseAccessUnusedBranchExtensionContract where
  sourceAnchor : String
  inputRegisters : BandedSparseAccessPaperRegisters
  activeImageIndex : Nat
  cleanInput : Bool
  validSparseBranch : Bool
  unusedSparseBranch : Bool
  unusedBranchImageRuleContract : BandedSparseAccessUnusedBranchImageRuleContract
  paperAgreementOnValidBranches : ObligationRecord
  unusedBranchImageRule : ObligationRecord
  unusedBranchInjective : ObligationRecord
  fullCleanDomainInjective : ObligationRecord
  daggerCleanup : ObligationRecord
  unitaryExtension : ObligationRecord
deriving Repr, DecidableEq

/--
Default unused-branch extension contract for one O_D^BS basis column.

All semantic fields remain false.  The record exists so later work can state
the reversible completion separately from the paper image on valid branches.
-/
def bandedSparseAccessUnusedBranchExtensionContract
    (p : OneTermRobinParameters) (j : Nat) :
    BandedSparseAccessUnusedBranchExtensionContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1 and one-term Robin zero-branch audit, arXiv:2506.20478"
  inputRegisters := bandedSparseAccessPaperRegisters p j
  activeImageIndex := bandedSparseAccessPaperImage p j
  cleanInput := bandedSparseAccessPaperCleanInput p j
  validSparseBranch := bandedSparseAccessPaperValidSparseBranch p j
  unusedSparseBranch := bandedSparseAccessPaperUnusedSparseBranch p j
  unusedBranchImageRuleContract :=
    bandedSparseAccessUnusedBranchImageRuleContract p j
  paperAgreementOnValidBranches := {
    description := "the extension agrees with the Lemma 1 image on valid row-dependent sparse branches"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }
  unusedBranchImageRule :=
    (bandedSparseAccessUnusedBranchImageRuleContract p j).imageSpecified
  unusedBranchInjective := {
    description := "the unused-branch image rule is injective on clean invalid branches"
    source := "QBE-AUTO-002 O_D^BS unused-branch extension contract"
    proved := false
  }
  fullCleanDomainInjective := {
    description := "valid-branch and unused-branch images are jointly injective on the full clean padded domain"
    source := "QBE-AUTO-002 O_D^BS unused-branch extension contract"
    proved := false
  }
  daggerCleanup := {
    description := "the dagger cleanup proof uses the reversible unused-branch extension where needed"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Lemma 1, arXiv:2506.20478"
    proved := false
  }
  unitaryExtension := {
    description := "the full O_D^BS matrix extends to a unitary on valid and unused clean branches"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- The unused-branch extension contract is obligation-only in Phase 1. -/
theorem bandedSparseAccessUnusedBranchExtensionContract_flags_false
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessUnusedBranchExtensionContract p j).paperAgreementOnValidBranches.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unusedBranchImageRule.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unusedBranchInjective.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).fullCleanDomainInjective.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).daggerCleanup.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unitaryExtension.proved = false := by
  simp [bandedSparseAccessUnusedBranchExtensionContract,
    bandedSparseAccessUnusedBranchImageRuleContract]

/--
The unused-branch contract classifies the recorded row-dependent boundary
collision without promoting any O_D^BS semantic proof flag.

The active global-slot image no longer has this concrete collision; the
extension fields remain false because this packet does not prove full
clean-domain injectivity, dagger cleanup, or unitarity.
-/
theorem bandedSparseAccessUnusedBranchExtensionContract_boundaryCollision_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperValidCleanSource p 0 = true ∧
      bandedSparseAccessPaperUnusedSparseBranch p 48 = true ∧
      bandedSparseAccessRowDependentPaperImage p 0 =
        bandedSparseAccessRowDependentPaperImage p 48 ∧
      bandedSparseAccessPaperImage p 0 ≠ bandedSparseAccessPaperImage p 48 ∧
      (bandedSparseAccessUnusedBranchExtensionContract p 48).unusedBranchInjective.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p 48).unitaryExtension.proved = false := by
  native_decide

/--
Package the unused-branch classifier with the reversible-extension obligations.

This is a contract bridge only: it exposes that an unused clean branch is in
the clean padded-input domain, is outside the row-dependent valid sparse-branch
classifier, and still has only false extension proof fields.
-/
theorem bandedSparseAccessUnusedBranchExtensionContract_of_unusedBranch
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperUnusedSparseBranch p j = true) :
    (bandedSparseAccessUnusedBranchExtensionContract p j).cleanInput = true ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).validSparseBranch = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unusedSparseBranch = true ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unusedBranchImageRule.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unusedBranchInjective.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).fullCleanDomainInjective.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).daggerCleanup.proved = false ∧
      (bandedSparseAccessUnusedBranchExtensionContract p j).unitaryExtension.proved = false := by
  have hclean :
      bandedSparseAccessPaperCleanInput p j = true :=
    bandedSparseAccessPaperUnusedSparseBranch_cleanInput_eq_true p j h
  have hvalid :
      bandedSparseAccessPaperValidSparseBranch p j = false :=
    bandedSparseAccessPaperUnusedSparseBranch_validSparseBranch_eq_false p j h
  simp [bandedSparseAccessUnusedBranchExtensionContract,
    bandedSparseAccessUnusedBranchImageRuleContract, h, hclean, hvalid]

/--
Paper-level wrapper for the full clean-domain extension obligation of
`O_D^BS`.

The paper clean domain contains every padded-zero source
`|0>^(n-l)|s>^l|i>^n`, including zero-amplitude sparse branches.  QBE currently
has only the active Lemma 1 image on valid row-dependent branches and a
per-column interface for clean unused branches.  This record lifts those
pieces into one contract without choosing a reversible unused-branch image and
without changing the active forward or dagger matrices.
-/
structure BandedSparseAccessFullCleanDomainExtensionContract where
  sourceAnchor : String
  cleanInputPredicate : String
  validSparseBranchPredicate : String
  validCleanSourcePredicate : String
  unusedSparseBranchPredicate : String
  unusedBranchImageRuleContract :
    Nat → BandedSparseAccessUnusedBranchImageRuleContract
  unusedBranchExtensionContract :
    Nat → BandedSparseAccessUnusedBranchExtensionContract
  cleanDomainSplit : ObligationRecord
  validBranchAgreement : ObligationRecord
  unusedBranchImageSpecified : ObligationRecord
  unusedBranchImageFinite : ObligationRecord
  unusedBranchInjective : ObligationRecord
  fullCleanDomainInjective : ObligationRecord
  daggerCleanup : ObligationRecord
  unitaryExtension : ObligationRecord

/--
Default full clean-domain extension contract for Lemma 1 `O_D^BS`.

All semantic fields are false obligations.  The nested per-column image-rule
contract still has `proposedImageIndex = none`, so this declaration only
records the missing proof interface for later source-domain reconciliation.
-/
def bandedSparseAccessFullCleanDomainExtensionContract
    (p : OneTermRobinParameters) :
    BandedSparseAccessFullCleanDomainExtensionContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1 and one-term Robin zero-branch audit, arXiv:2506.20478"
  cleanInputPredicate := "bandedSparseAccessPaperCleanInput"
  validSparseBranchPredicate := "bandedSparseAccessPaperValidSparseBranch"
  validCleanSourcePredicate := "bandedSparseAccessPaperValidCleanSource"
  unusedSparseBranchPredicate := "bandedSparseAccessPaperUnusedSparseBranch"
  unusedBranchImageRuleContract := fun j =>
    bandedSparseAccessUnusedBranchImageRuleContract p j
  unusedBranchExtensionContract := fun j =>
    bandedSparseAccessUnusedBranchExtensionContract p j
  cleanDomainSplit := {
    description := "the full padded clean domain is partitioned into valid nonzero-stencil branches and clean unused sparse branches"
    source := "QBE-AUTO-002 O_D^BS full clean-domain extension contract"
    proved := false
  }
  validBranchAgreement := {
    description := "the full extension agrees with the Lemma 1 image on every valid clean sparse branch"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }
  unusedBranchImageSpecified := {
    description := "a faithful reversible image rule is specified for every clean unused sparse branch"
    source := "QBE-AUTO-002 O_D^BS full clean-domain extension contract"
    proved := false
  }
  unusedBranchImageFinite := {
    description := "every specified unused-branch image is a finite one-term Robin basis index"
    source := "QBE-AUTO-002 O_D^BS full clean-domain extension contract"
    proved := false
  }
  unusedBranchInjective := {
    description := "the unused-branch image rule is injective on clean invalid sparse branches"
    source := "QBE-AUTO-002 O_D^BS full clean-domain extension contract"
    proved := false
  }
  fullCleanDomainInjective := {
    description := "valid-branch and unused-branch images are jointly injective on the full padded clean domain"
    source := "QBE-AUTO-002 O_D^BS full clean-domain extension contract"
    proved := false
  }
  daggerCleanup := {
    description := "the dagger cleanup proof is valid for the full padded clean domain"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Lemma 1, arXiv:2506.20478"
    proved := false
  }
  unitaryExtension := {
    description := "the full clean-domain image rule extends to a unitary O_D^BS matrix"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- The full clean-domain wrapper is obligation-only in Phase 1. -/
theorem bandedSparseAccessFullCleanDomainExtensionContract_flags_false
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessFullCleanDomainExtensionContract p).cleanDomainSplit.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).validBranchAgreement.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageSpecified.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageFinite.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchInjective.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).fullCleanDomainInjective.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).daggerCleanup.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unitaryExtension.proved = false ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).proposedImageIndex = none ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).imageSpecified.proved = false ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).imageFinite.proved = false := by
  simp [bandedSparseAccessFullCleanDomainExtensionContract,
    bandedSparseAccessUnusedBranchImageRuleContract]

/--
The full clean-domain wrapper reuses the existing per-column unused-branch
classifier bridge and keeps every extension proof flag false.
-/
theorem bandedSparseAccessFullCleanDomainExtensionContract_of_unusedBranch
    (p : OneTermRobinParameters) (j : Nat)
    (h : bandedSparseAccessPaperUnusedSparseBranch p j = true) :
    ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).cleanInput = true ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).validSparseBranch = false ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).unusedSparseBranch = true ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract j).proposedImageIndex = none ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageSpecified.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).fullCleanDomainInjective.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unitaryExtension.proved = false := by
  have hclean :
      bandedSparseAccessPaperCleanInput p j = true :=
    bandedSparseAccessPaperUnusedSparseBranch_cleanInput_eq_true p j h
  have hvalid :
      bandedSparseAccessPaperValidSparseBranch p j = false :=
    bandedSparseAccessPaperUnusedSparseBranch_validSparseBranch_eq_false p j h
  simp [bandedSparseAccessFullCleanDomainExtensionContract,
    bandedSparseAccessUnusedBranchImageRuleContract, h, hclean, hvalid]

/--
Wrapper-facing form of the local clean-domain split audit.

The classifier split is Lean-proved, while the full semantic wrapper still
keeps `cleanDomainSplit.proved = false` because no unused-branch image rule,
injectivity proof, or unitary extension has been supplied.
-/
theorem bandedSparseAccessFullCleanDomainExtensionContract_localCleanDomainSplit
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperCleanInput p j = true ↔
      bandedSparseAccessPaperValidCleanSource p j = true ∨
        bandedSparseAccessPaperUnusedSparseBranch p j = true) ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).cleanDomainSplit.proved =
        false := by
  exact ⟨bandedSparseAccessPaperCleanDomainSplit_iff p j, rfl⟩

/--
Lean-facing source decision for unused zero-amplitude `O_D^BS` branches.

Cycle 14 records that no paper-backed image formula and no accepted external
reversible-extension theorem currently supplies the missing image rule for
clean unused sparse branches.  This is a blocking dependency record, not a new
oracle construction.
-/
structure BandedSparseAccessUnusedZeroBranchSourceDecision where
  sourceAnchor : String
  citedResultKey : String
  paperImageRuleSpecified : Bool
  externalExtensionTheoremAccepted : Bool
  lowerProofSearchAllowed : Bool
  dependency : ObligationRecord
deriving Repr, DecidableEq

/--
Default cycle-14 source decision for unused zero-amplitude sparse branches.

The false Boolean fields deliberately prevent lower proof work from treating
the current colliding active image as a permutation or unitary extension.
-/
def bandedSparseAccessUnusedZeroBranchSourceDecision :
    BandedSparseAccessUnusedZeroBranchSourceDecision where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1 and Fig. 1-term Robin, arXiv:2506.20478"
  citedResultKey := "QBE.ODBS.UnusedZeroBranchExtension"
  paperImageRuleSpecified := false
  externalExtensionTheoremAccepted := false
  lowerProofSearchAllowed := false
  dependency := {
    description := "unused zero-amplitude sparse branches need a paper-backed image rule or accepted reversible-extension theorem before O_D^BS injectivity, cleanup, or unitarity proof search"
    source := "research-wiki/cited-results/GHL2025.md: QBE.ODBS.UnusedZeroBranchExtension"
    proved := false
  }

/-- The cycle-14 source decision is a blocking obligation, not a proof ticket. -/
theorem bandedSparseAccessUnusedZeroBranchSourceDecision_flags_false :
    bandedSparseAccessUnusedZeroBranchSourceDecision.paperImageRuleSpecified = false ∧
      bandedSparseAccessUnusedZeroBranchSourceDecision.externalExtensionTheoremAccepted = false ∧
      bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed = false ∧
      bandedSparseAccessUnusedZeroBranchSourceDecision.dependency.proved = false := by
  simp [bandedSparseAccessUnusedZeroBranchSourceDecision]

/--
The source decision keeps the full clean-domain wrapper in obligation mode.

This ties the cited-results dependency to the existing wrapper fields without
changing any active matrix or promoting any semantic proof flag.
-/
theorem bandedSparseAccessUnusedZeroBranchSourceDecision_keepsFullDomainFlagsFalse
    (p : OneTermRobinParameters) :
    bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageSpecified.proved =
        false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).fullCleanDomainInjective.proved =
        false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).daggerCleanup.proved =
        false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unitaryExtension.proved =
        false := by
  simp [bandedSparseAccessUnusedZeroBranchSourceDecision,
    bandedSparseAccessFullCleanDomainExtensionContract]

/--
The blocking source decision keeps every unused-branch image slot unspecified.

This is a guard for later lower packets: disabling proof search also means the
per-column image-rule contract and the full-domain wrapper still expose
`proposedImageIndex = none` with false image-rule obligations.
-/
theorem bandedSparseAccessUnusedZeroBranchSourceDecision_keepsImageRuleUnspecified
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed = false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).proposedImageIndex = none ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).imageSpecified.proved = false ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract
        j).proposedImageIndex = none ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract
        j).imageSpecified.proved = false ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract
        j).separatesActiveCollision.proved = false := by
  simp [bandedSparseAccessUnusedZeroBranchSourceDecision,
    bandedSparseAccessFullCleanDomainExtensionContract,
    bandedSparseAccessUnusedBranchImageRuleContract]

/--
The blocking source decision also keeps the paper-level O_D^BS contract
obligations false.

This is separate from the full clean-domain wrapper: it pins the original
Lemma 1 contract fields that a later proof packet would otherwise try to close.
-/
theorem bandedSparseAccessUnusedZeroBranchSourceDecision_keepsPaperContractFlagsFalse
    (p : OneTermRobinParameters) :
    bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed = false ∧
      (defaultBandedSparseAccessPaperContract p).forwardCorrect.proved = false ∧
      (defaultBandedSparseAccessPaperContract p).daggerCleanup.proved = false ∧
      (defaultBandedSparseAccessPaperContract p).unitaryExtension.proved = false := by
  simp [bandedSparseAccessUnusedZeroBranchSourceDecision,
    defaultBandedSparseAccessPaperContract]

/--
Source transcript for the Robin zero-inclusion sentence near Theorem 1.

The paper states that zeros may be included in the sparse enumeration and then
uses the range `s = 0, ..., kappa - 1` in Eq. ROBIN clarified.  This source
fact explains why the row-dependent nonzero-stencil classifier is not a
faithful full domain restriction.  It still does not choose an injective image
for clean unused zero-amplitude branches.
-/
structure BandedSparseAccessRobinZeroInclusionSourceContract where
  sourceAnchor : String
  zeroInclusionAnchor : String
  equationAnchor : String
  sparseIndexRange : String
  zerosIncludedInSparseEnumeration : Bool
  paperImageEquation : String
  unusedBranchImageRule : Option String
  unusedBranchImageIndex : Option Nat
  reversibleExtensionTheorem : Option String
  closesUnusedZeroBranchExtension : Bool
  lowerProofSearchAllowed : Bool
  imageRuleObligation : ObligationRecord
  reversibleExtensionObligation : ObligationRecord
deriving Repr, DecidableEq

/--
Default transcript of the GHL2025 Robin zero-inclusion source text.

The source records that zero-amplitude sparse branches remain in the
kappa-wide sparse register.  The missing image rule and any reversible
extension theorem are intentionally absent, so this declaration does not
unblock O_D^BS proof search.
-/
def bandedSparseAccessRobinZeroInclusionSourceContract :
    BandedSparseAccessRobinZeroInclusionSourceContract where
  sourceAnchor :=
    "Guseynov-Huang-Liu 2025, one-term Robin construction, arXiv:2506.20478"
  zeroInclusionAnchor :=
    "text before Theorem 1-term Robin: zeros can be included in the set of non-zero elements"
  equationAnchor :=
    "Lemma 1 and Eq. ROBIN clarified, arXiv:2506.20478"
  sparseIndexRange := "s = 0, ..., kappa - 1"
  zerosIncludedInSparseEnumeration := true
  paperImageEquation := "O_D^BS |0>^(n-l)|s>^l|i>^n = |r_si>^n|i>^n"
  unusedBranchImageRule := none
  unusedBranchImageIndex := none
  reversibleExtensionTheorem := none
  closesUnusedZeroBranchExtension := false
  lowerProofSearchAllowed := false
  imageRuleObligation := {
    description := "the Robin source includes zero-amplitude sparse branches but does not specify their injective reversible image"
    source := "Guseynov-Huang-Liu 2025, one-term Robin construction and Lemma 1, arXiv:2506.20478"
    proved := false
  }
  reversibleExtensionObligation := {
    description := "no cited reversible-extension theorem is accepted for the unused zero-amplitude sparse branches"
    source := "research-wiki/cited-results/GHL2025.md: QBE.ODBS.UnusedZeroBranchExtension"
    proved := false
  }

/--
The Robin zero-inclusion source transcript keeps the unused-branch route
blocked.

This guard records the exact source-backed inclusion of zero-amplitude sparse
branches while preserving the absence of a branch image rule or reversible
extension theorem.
-/
theorem bandedSparseAccessRobinZeroInclusionSourceContract_blocks_unusedZeroBranch :
    bandedSparseAccessRobinZeroInclusionSourceContract.zerosIncludedInSparseEnumeration =
        true ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.unusedBranchImageRule =
        none ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.unusedBranchImageIndex =
        none ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.reversibleExtensionTheorem =
        none ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.closesUnusedZeroBranchExtension =
        false ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.lowerProofSearchAllowed =
        false ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.imageRuleObligation.proved =
        false ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.reversibleExtensionObligation.proved =
        false ∧
      bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed =
        false := by
  simp [bandedSparseAccessRobinZeroInclusionSourceContract,
    bandedSparseAccessUnusedZeroBranchSourceDecision]

/--
The zero-inclusion transcript does not fill the per-column image-rule slot.

For every one-term parameter choice and source column, the direct image-rule
contract remains unspecified while lower proof search is disabled.
-/
theorem bandedSparseAccessRobinZeroInclusionSourceContract_keepsImageRuleUnspecified
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessRobinZeroInclusionSourceContract.zerosIncludedInSparseEnumeration =
        true ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.unusedBranchImageIndex =
        none ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.reversibleExtensionTheorem =
        none ∧
      bandedSparseAccessRobinZeroInclusionSourceContract.lowerProofSearchAllowed =
        false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).proposedImageIndex =
        none ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).imageSpecified.proved =
        false := by
  simp [bandedSparseAccessRobinZeroInclusionSourceContract,
    bandedSparseAccessUnusedBranchImageRuleContract]

/--
Source contract imported from the prior PDE block-encoding paper.

The prior paper supplies the same padded-register equation and an appendix
decomposition into a first-row index unitary and modular addition.  This record
is intentionally only a source transcript: it does not provide a Robin-specific
image rule for clean unused zero-amplitude sparse branches.
-/
structure BandedSparseAccessPriorPDESourceContract where
  sourceAnchor : String
  definitionAnchor : String
  lemmaAnchor : String
  appendixAnchor : String
  oracleEquation : String
  circuitDecomposition : String
  resourceClaim : ObligationRecord
  robinUnusedBranchImageRule : Option String
  closesUnusedZeroBranchExtension : Bool
  lowerProofSearchAllowed : Bool
deriving Repr, DecidableEq

/--
Default transcript of arXiv:2405.12855v3 Definition 6, Lemma 1, and the
appendix construction for `O_A^BS`.

The field `robinUnusedBranchImageRule = none` records the audit result: this
source supports the imported sparse-access primitive, but not the missing
Robin unused-branch image formula.
-/
def bandedSparseAccessPriorPDESourceContract :
    BandedSparseAccessPriorPDESourceContract where
  sourceAnchor :=
    "Guseynov-Huang-Liu 2024, arXiv:2405.12855v3, Definition 6, Lemma 1, Appendix Banded-sparse-access"
  definitionAnchor := "Definition 6: Banded-sparse-access"
  lemmaAnchor := "Lemma 1: Banded-sparse-access resource bound"
  appendixAnchor := "Appendix: Explicit quantum circuit construction for O_A^BS"
  oracleEquation := "O_A^BS |0>^(n-l)|s>^l|i>^n = |r_si>^n|i>^n"
  circuitDecomposition := "O_A^BS = U^SUM (U_A^(l) tensor I^n)"
  resourceClaim := {
    description := "transcribe the prior-paper gate and pure-ancilla resource counts for the padded banded-sparse-access primitive"
    source := "Guseynov-Huang-Liu 2024, arXiv:2405.12855v3, Lemma 1"
    proved := false
  }
  robinUnusedBranchImageRule := none
  closesUnusedZeroBranchExtension := false
  lowerProofSearchAllowed := false

/--
The explicit citation chain for the displayed Robin sparse-address equation.
Lemma 2 of arXiv:2506.20478 invokes Lemma 1 of arXiv:2405.12855; older
transcript fields above retain their historical labels for drift auditing.
-/
def robinBandedSparseAccessCitationChain : List String := [
  "Guseynov-Huang-Liu 2025, arXiv:2506.20478, Lemma 2",
  "Guseynov-Huang-Liu 2024, arXiv:2405.12855v3, Lemma 1"
]

@[simp] theorem robinBandedSparseAccessCitationChain_eq :
    robinBandedSparseAccessCitationChain = [
      "Guseynov-Huang-Liu 2025, arXiv:2506.20478, Lemma 2",
      "Guseynov-Huang-Liu 2024, arXiv:2405.12855v3, Lemma 1"
    ] := rfl

/--
The prior PDE source does not unblock the QBE unused-zero-branch extension.

This is the compiled guard for the source audit: the cited theorem is recorded,
but lower proof search for Robin unused-branch injectivity, cleanup, and
unitarity remains disabled.
-/
theorem bandedSparseAccessPriorPDESourceContract_blocks_unusedZeroBranch :
    bandedSparseAccessPriorPDESourceContract.robinUnusedBranchImageRule = none ∧
      bandedSparseAccessPriorPDESourceContract.closesUnusedZeroBranchExtension = false ∧
      bandedSparseAccessPriorPDESourceContract.lowerProofSearchAllowed = false ∧
      bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed = false := by
  simp [bandedSparseAccessPriorPDESourceContract,
    bandedSparseAccessUnusedZeroBranchSourceDecision]

/-- The prior PDE source contract records the exact sparse-access equation. -/
theorem bandedSparseAccessPriorPDESourceContract_oracleEquation :
    bandedSparseAccessPriorPDESourceContract.oracleEquation =
      "O_A^BS |0>^(n-l)|s>^l|i>^n = |r_si>^n|i>^n" := rfl

/-- The prior PDE resource claim remains an external obligation in QBE. -/
theorem bandedSparseAccessPriorPDESourceContract_resource_unproved :
    bandedSparseAccessPriorPDESourceContract.resourceClaim.proved = false := rfl

/--
Boolean form of the Lemma 1 clean-input domain.

The executable predicate is exactly the statement that the padded part of the
`O_D^BS` sparse-address register is zero.  This only classifies columns; it
does not prove the clean-input source equation or a unitary extension.
-/
theorem bandedSparseAccessPaperCleanInput_iff
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperCleanInput p j = true ↔
      (bandedSparseAccessPaperRegisters p j).paddedZeroValue = 0 := by
  unfold bandedSparseAccessPaperCleanInput
  exact beq_iff_eq

/--
Per-column audit record for the executable Lemma 1 paper image.

This records the source-domain flag, the image index, and the two register
properties expected from the paper equation.  The Boolean fields are executable
checks for the current skeleton; they are not promoted to theorem-level
correctness.  The obligation fields keep the clean-domain and full-unitary
extension gaps explicit.
-/
structure BandedSparseAccessPaperColumnContract where
  sourceAnchor : String
  inputRegisters : BandedSparseAccessPaperRegisters
  cleanInput : Bool
  imageIndex : Nat
  imageRegisters : BandedSparseAccessPaperRegisters
  rowPreserved : Bool
  addressWritten : Bool
  addressInRange : Bool
  imageNoSpill : Bool
  cleanInputDomain : ObligationRecord
  addressRange : ObligationRecord
  noSpill : ObligationRecord
  unitaryExtension : ObligationRecord
deriving Repr, DecidableEq

/--
Default per-column contract for the `O_D^BS` paper image skeleton.
-/
def bandedSparseAccessPaperColumnContract
    (p : OneTermRobinParameters) (j : Nat) :
    BandedSparseAccessPaperColumnContract :=
  let regs := bandedSparseAccessPaperRegisters p j
  let image := bandedSparseAccessPaperImage p j
  let imageRegs := bandedSparseAccessPaperRegisters p image
  let paperContract := defaultBandedSparseAccessPaperContract p
  {
    sourceAnchor := paperContract.sourceAnchor
    inputRegisters := regs
    cleanInput := bandedSparseAccessPaperCleanInput p j
    imageIndex := image
    imageRegisters := imageRegs
    rowPreserved := imageRegs.rowValue == regs.rowValue
    addressWritten := imageRegs.odRegisterValue == bandedSparseAccessPaperAddress p j
    addressInRange := bandedSparseAccessPaperAddressInRange p j
    imageNoSpill := bandedSparseAccessPaperImageNoSpill p j
    cleanInputDomain := paperContract.cleanInputDomain
    addressRange := paperContract.addressRange
    noSpill := paperContract.noSpill
    unitaryExtension := paperContract.unitaryExtension
  }

/-- The per-column contract uses the shared Lemma 1 register extractor. -/
theorem bandedSparseAccessPaperColumnContract_inputRegisters_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).inputRegisters =
      bandedSparseAccessPaperRegisters p j := rfl

/-- The per-column clean-domain flag is the executable padded-zero predicate. -/
theorem bandedSparseAccessPaperColumnContract_cleanInput_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).cleanInput =
      bandedSparseAccessPaperCleanInput p j := rfl

/--
The per-column clean-domain flag is true exactly on Lemma 1 clean columns.

Columns with a nonzero padded register are still covered only by the explicit
unitary-extension obligation.
-/
theorem bandedSparseAccessPaperColumnContract_cleanInput_iff
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).cleanInput = true ↔
      (bandedSparseAccessPaperRegisters p j).paddedZeroValue = 0 := by
  rw [bandedSparseAccessPaperColumnContract_cleanInput_eq]
  exact bandedSparseAccessPaperCleanInput_iff p j

/--
The per-column audit keeps the full-space unitary extension as an open
obligation for every column, including non-clean padded-register inputs.
-/
theorem bandedSparseAccessPaperColumnContract_unitaryExtension_proved_eq_false
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).unitaryExtension.proved = false := rfl

/-- The per-column contract records the same image index as the paper-image skeleton. -/
theorem bandedSparseAccessPaperColumnContract_imageIndex_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).imageIndex =
      bandedSparseAccessPaperImage p j := rfl

/-- The per-column contract records the executable n-bit address range check. -/
theorem bandedSparseAccessPaperColumnContract_addressInRange_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).addressInRange =
      bandedSparseAccessPaperAddressInRange p j := rfl

/-- The per-column contract records the executable high-bit no-spill check. -/
theorem bandedSparseAccessPaperColumnContract_imageNoSpill_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).imageNoSpill =
      bandedSparseAccessPaperImageNoSpill p j := rfl

/--
The per-column audit records that the paper image preserves the row register.

This is an executable register-safety fact for the Phase 1 skeleton; it does
not promote the paper-level `forwardCorrect` obligation.
-/
theorem bandedSparseAccessPaperColumnContract_rowPreserved_eq_true
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperColumnContract p j).rowPreserved = true := by
  unfold bandedSparseAccessPaperColumnContract
  simp [bandedSparseAccessPaperImage_rowValue_eq]

/--
The per-column audit records that the paper image writes the O_D register to
the computed address whenever that address is an n-bit value.
-/
theorem bandedSparseAccessPaperColumnContract_addressWritten_eq_true_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    (bandedSparseAccessPaperColumnContract p j).addressWritten = true := by
  unfold bandedSparseAccessPaperColumnContract
  simp [bandedSparseAccessPaperImage_odRegisterValue_eq p j haddr]

/-- The per-column address-range audit Boolean follows from the address bound. -/
theorem bandedSparseAccessPaperColumnContract_addressInRange_eq_true_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    (bandedSparseAccessPaperColumnContract p j).addressInRange = true := by
  rw [bandedSparseAccessPaperColumnContract_addressInRange_eq]
  exact (bandedSparseAccessPaperAddressInRange_iff p j).2 haddr

/-- The per-column no-spill audit Boolean follows from the address bound. -/
theorem bandedSparseAccessPaperColumnContract_imageNoSpill_eq_true_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    (bandedSparseAccessPaperColumnContract p j).imageNoSpill = true := by
  rw [bandedSparseAccessPaperColumnContract_imageNoSpill_eq]
  exact bandedSparseAccessPaperImageNoSpill_eq_true_of_address_lt p j haddr

/--
Reusable per-column register-safety package for the active Lemma 1 image
skeleton.  The package is deliberately conditional on the existing n-bit
address hypothesis, so it does not hide the paper parameter-family obligation.
-/
theorem bandedSparseAccessPaperColumnContract_registerSafety_of_address_lt
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    (bandedSparseAccessPaperColumnContract p j).rowPreserved = true ∧
      (bandedSparseAccessPaperColumnContract p j).addressWritten = true ∧
      (bandedSparseAccessPaperColumnContract p j).addressInRange = true ∧
      (bandedSparseAccessPaperColumnContract p j).imageNoSpill = true := by
  exact ⟨
    bandedSparseAccessPaperColumnContract_rowPreserved_eq_true p j,
    bandedSparseAccessPaperColumnContract_addressWritten_eq_true_of_address_lt p j haddr,
    bandedSparseAccessPaperColumnContract_addressInRange_eq_true_of_address_lt p j haddr,
    bandedSparseAccessPaperColumnContract_imageNoSpill_eq_true_of_address_lt p j haddr⟩

/--
Matrix entries for the faithful Lemma 1 `O_D^BS` paper-image skeleton.

The column `j` has a candidate `1` entry at
`bandedSparseAccessPaperImage p j.val`, which replaces the padded sparse-address
register by `r_si` and preserves the row register.  This declaration is the
active `oneTermRobinGate_O_D_BS` matrix, but it does not prove that the image is
in range, injective, unitary, or cleaned up by the dagger.
-/
def bandedSparseAccessPaperMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    if i.val = bandedSparseAccessPaperImage p j.val then Coeff.rat 1 else Coeff.rat 0

/-- The paper-image matrix entry is governed by `bandedSparseAccessPaperImage`. -/
theorem bandedSparseAccessPaperMatrix_eq_image (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    bandedSparseAccessPaperMatrix p i j =
      if i.val = bandedSparseAccessPaperImage p j.val then Coeff.rat 1 else Coeff.rat 0 := by
  rfl

/--
Forward paper-image matrix entry at the finite image column.

The hypotheses are the same explicit range hypotheses used to construct
`bandedSparseAccessPaperImageFin`.  This theorem does not assert that the
image function is injective or that the matrix is unitary.
-/
theorem bandedSparseAccessPaperMatrix_imageFin_eq_one
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    bandedSparseAccessPaperMatrix p (bandedSparseAccessPaperImageFin p j haddr) j =
      Coeff.rat 1 := by
  simp [bandedSparseAccessPaperMatrix, bandedSparseAccessPaperImageFin]

/--
Transpose-style matrix for the faithful Lemma 1 `O_D^BS` paper-image skeleton.

The entry `M†[i,j]` is `1` exactly when column index `j` is the forward
paper image of row index `i`.  This is only the matrix-level transpose of the
current executable image skeleton; the inverse, unitarity, and post-SWAP cleanup
claims remain tracked by `defaultBandedSparseAccessPaperContract p` with
`proved := false`.
-/
def bandedSparseAccessPaperDaggerMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    if j.val = bandedSparseAccessPaperImage p i.val then Coeff.rat 1 else Coeff.rat 0

/-- The paper-image dagger matrix is the transpose-style matrix for the image skeleton. -/
theorem bandedSparseAccessPaperDaggerMatrix_eq_image (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    bandedSparseAccessPaperDaggerMatrix p i j =
      if j.val = bandedSparseAccessPaperImage p i.val then Coeff.rat 1 else Coeff.rat 0 := by
  rfl

/--
Transpose-style paper-image matrix entry paired with the finite forward image.

This is the entry relation needed before an inverse-on-range proof.  It does
not prove that the transpose-style matrix cleans the ancillas after SWAP.
-/
theorem bandedSparseAccessPaperDaggerMatrix_imageFin_eq_one
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    bandedSparseAccessPaperDaggerMatrix p j (bandedSparseAccessPaperImageFin p j haddr) =
      Coeff.rat 1 := by
  simp [bandedSparseAccessPaperDaggerMatrix, bandedSparseAccessPaperImageFin]

/--
Sparse amplitude value: the s-th nonzero stencil coefficient of row i in the
Robin derivative matrix, returned as a Coeff value.

This is the data layer that both O_DT^S (sparse amplitude oracle, Lemma 3)
and Ry_boundary (boundary-controlled rotations) need.  The column index
corresponding to each (s, i) pair is given by `robinSparseColumnMap`.

For the fourth-order central second-derivative stencil:
- Bulk rows (K1 ≤ i ≤ K2): 5 entries at offsets {-2,-1,0,1,2}
- Left boundary row 0: 3 entries with Robin correction (A1*dx term)
- Left boundary row 1: 4 entries with Robin correction (A1*dx term)
- Right boundary row N-2: 4 entries with Robin correction (B1*dx term)
- Right boundary row N-1: 3 entries with Robin correction (B1*dx term)
- Unused sparse indices (s ≥ entry count): Coeff.rat 0

main.tex:822-849, 1081-1083, 1113-1117 --/
def robinSparseAmplitudeValue (n s i : Nat) : Coeff :=
  let N := gridSize n
  let K1 := 2
  let K2 := N - 3
  if K1 ≤ i ∧ i ≤ K2 then
    match s with
    | 0 => Coeff.rat ((-1 : Rat) / 12)
    | 1 => Coeff.rat ((4 : Rat) / 3)
    | 2 => Coeff.rat ((-5 : Rat) / 2)
    | 3 => Coeff.rat ((4 : Rat) / 3)
    | 4 => Coeff.rat ((-1 : Rat) / 12)
    | _ => Coeff.rat 0
  else if i = 0 then
    match s with
    | 0 => Coeff.add (Coeff.rat ((-5 : Rat) / 2))
        (Coeff.mul (Coeff.rat ((7 : Rat) / 3)) (Coeff.symbol "A1*dx"))
    | 1 => Coeff.rat ((8 : Rat) / 3)
    | 2 => Coeff.rat ((-1 : Rat) / 6)
    | _ => Coeff.rat 0
  else if i = 1 then
    match s with
    | 0 => Coeff.add (Coeff.rat ((4 : Rat) / 3))
        (Coeff.neg (Coeff.mul (Coeff.rat ((1 : Rat) / 6)) (Coeff.symbol "A1*dx")))
    | 1 => Coeff.rat ((-31 : Rat) / 12)
    | 2 => Coeff.rat ((4 : Rat) / 3)
    | 3 => Coeff.rat ((-1 : Rat) / 12)
    | _ => Coeff.rat 0
  else if i = N - 2 then
    match s with
    | 0 => Coeff.rat ((-1 : Rat) / 12)
    | 1 => Coeff.rat ((4 : Rat) / 3)
    | 2 => Coeff.rat ((-31 : Rat) / 12)
    | 3 => Coeff.add (Coeff.rat ((4 : Rat) / 3))
        (Coeff.mul (Coeff.rat ((1 : Rat) / 6)) (Coeff.symbol "B1*dx"))
    | _ => Coeff.rat 0
  else if i = N - 1 then
    match s with
    | 0 => Coeff.rat ((-1 : Rat) / 6)
    | 1 => Coeff.rat ((8 : Rat) / 3)
    | 2 => Coeff.add (Coeff.rat ((-5 : Rat) / 2))
        (Coeff.neg (Coeff.mul (Coeff.rat ((7 : Rat) / 3)) (Coeff.symbol "B1*dx")))
    | _ => Coeff.rat 0
  else
    Coeff.rat 0

/--
Global sparse-slot coefficient source for the one-term Robin table.

Unlike `robinSparseAmplitudeValue`, the sparse index is interpreted through
the active global slot table used by `oneTermRobinGlobalSparseAddress`.
Thus slot `2` is the zero-offset diagonal slot in every row. Boundary slots
that are present in the global sparse register but absent from the Robin row
carry coefficient `0`; the slot itself is not deleted.
Guseynov-Huang-Liu 2025, Lemma `Diagonal sparsity`, Lemma
`Banded-sparse-access-oracle`, the zero-inclusion paragraph before Theorem
`1 term robin`, and Eq. `ROBIN clarified`, arXiv:2506.20478.
-/
def robinGlobalSparseAmplitudeValue (n s i : Nat) : Coeff :=
  let N := gridSize n
  let K1 := 2
  let K2 := N - 3
  if K1 ≤ i ∧ i ≤ K2 then
    match s with
    | 0 => Coeff.rat ((-1 : Rat) / 12)
    | 1 => Coeff.rat ((4 : Rat) / 3)
    | 2 => Coeff.rat ((-5 : Rat) / 2)
    | 3 => Coeff.rat ((4 : Rat) / 3)
    | 4 => Coeff.rat ((-1 : Rat) / 12)
    | _ => Coeff.rat 0
  else if i = 0 then
    match s with
    | 2 => Coeff.add (Coeff.rat ((-5 : Rat) / 2))
        (Coeff.mul (Coeff.rat ((7 : Rat) / 3)) (Coeff.symbol "A1*dx"))
    | 3 => Coeff.rat ((8 : Rat) / 3)
    | 4 => Coeff.rat ((-1 : Rat) / 6)
    | _ => Coeff.rat 0
  else if i = 1 then
    match s with
    | 1 => Coeff.add (Coeff.rat ((4 : Rat) / 3))
        (Coeff.neg (Coeff.mul (Coeff.rat ((1 : Rat) / 6)) (Coeff.symbol "A1*dx")))
    | 2 => Coeff.rat ((-31 : Rat) / 12)
    | 3 => Coeff.rat ((4 : Rat) / 3)
    | 4 => Coeff.rat ((-1 : Rat) / 12)
    | _ => Coeff.rat 0
  else if i = N - 2 then
    match s with
    | 0 => Coeff.rat ((-1 : Rat) / 12)
    | 1 => Coeff.rat ((4 : Rat) / 3)
    | 2 => Coeff.rat ((-31 : Rat) / 12)
    | 3 => Coeff.add (Coeff.rat ((4 : Rat) / 3))
        (Coeff.mul (Coeff.rat ((1 : Rat) / 6)) (Coeff.symbol "B1*dx"))
    | _ => Coeff.rat 0
  else if i = N - 1 then
    match s with
    | 0 => Coeff.rat ((-1 : Rat) / 6)
    | 1 => Coeff.rat ((8 : Rat) / 3)
    | 2 => Coeff.add (Coeff.rat ((-5 : Rat) / 2))
        (Coeff.neg (Coeff.mul (Coeff.rat ((7 : Rat) / 3)) (Coeff.symbol "B1*dx")))
    | _ => Coeff.rat 0
  else
    Coeff.rat 0

/-- Focused boundary regression: global slot `2` is the row-`0` diagonal. -/
theorem robinGlobalSparseAmplitudeValue_boundarySlot2_row0_n3 :
    robinGlobalSparseAmplitudeValue 3 2 0 =
      Coeff.add (Coeff.rat ((-5 : Rat) / 2))
        (Coeff.mul (Coeff.rat ((7 : Rat) / 3)) (Coeff.symbol "A1*dx")) := by
  native_decide

/--
The focused global slot is not the old row-local sparse entry.

This records the contract drift found by the gamma3 boundary packet without
promoting any analytic normalizer or block-encoding flag.
-/
theorem robinGlobalSparseAmplitudeValue_boundarySlot2_differs_rowLocal_n3 :
    robinGlobalSparseAmplitudeValue 3 2 0 ≠
      robinSparseAmplitudeValue 3 2 0 := by
  native_decide

/--
Shared Phase-1 contract for every paper route that uses the normalized
derivative coefficient `D_j^(s) / N_D`.

Both Lemma 3 `O_DT^S` and the boundary `R_y` angle formulas use the same
global sparse-slot coefficient source and the same normalizer symbol `N_D`.
This record keeps the common analytic gaps in one Lean object: nonzero normalizer, division
semantics, coefficient bound, absolute-square semantics, square-root
complement, arccos semantics, and two-by-two unitarity.  It is a contract
only; every obligation is false in Phase 1.
Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), Fig. 1-term Robin, and boundary
rotation equations, arXiv:2506.20478.
-/
structure DerivativeNormalizerNDContract where
  sourceAnchor : String
  rowValue : Nat
  sparseIndexValue : Nat
  coefficient : Coeff
  normalizerND : Coeff
  normalizedCoefficient : Coeff
  normalizedCoefficientFormula : String
  nonzeroNormalizer : ObligationRecord
  divisionSemantics : ObligationRecord
  coefficientBound : ObligationRecord
  absSquareSemantics : ObligationRecord
  sqrtComplementSemantics : ObligationRecord
  arccosSemantics : ObligationRecord
  twoByTwoUnitary : ObligationRecord
deriving Repr, DecidableEq

/--
Default shared `N_D` normalizer contract for one Robin coefficient.

The normalized coefficient is represented by multiplying the sparse derivative
coefficient by the formal symbol `N_D_inv`.  This is not a proof that `N_D` is
nonzero or that a division operation has been interpreted.
-/
def derivativeNormalizerNDContract
    (p : OneTermRobinParameters) (row sparse : Nat) :
    DerivativeNormalizerNDContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), Fig. 1-term Robin, and boundary Ry equations, arXiv:2506.20478"
  rowValue := row
  sparseIndexValue := sparse
  coefficient := robinGlobalSparseAmplitudeValue p.n sparse row
  normalizerND := Coeff.symbol "N_D"
  normalizedCoefficient :=
    Coeff.mul (robinGlobalSparseAmplitudeValue p.n sparse row) (Coeff.symbol "N_D_inv")
  normalizedCoefficientFormula := "D_j^(s) / N_D"
  nonzeroNormalizer := {
    description := "prove N_D is nonzero before interpreting D_j^(s) / N_D"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  divisionSemantics := {
    description := "interpret the formal coefficient times N_D_inv as D_j^(s) / N_D"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  coefficientBound := {
    description := "prove the N_D bound needed for normalized derivative coefficients"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), and boundary Ry equations, arXiv:2506.20478"
    proved := false
  }
  absSquareSemantics := {
    description := "interpret |D_j^(s)|^2 / N_D^2 for Eq. (20)"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  sqrtComplementSemantics := {
    description := "prove the square-root complementary amplitude from the N_D bound"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  arccosSemantics := {
    description := "place D_j^(s) / N_D in the real arccos domain for boundary Ry"
    source := "Guseynov-Huang-Liu 2025, boundary Ry angle equations, arXiv:2506.20478"
    proved := false
  }
  twoByTwoUnitary := {
    description := "prove the two-by-two rotation block is unitary under the N_D bound"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), and boundary Ry equations, arXiv:2506.20478"
    proved := false
  }

theorem derivativeNormalizerNDContract_coefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDContract p row sparse).coefficient =
      robinGlobalSparseAmplitudeValue p.n sparse row := rfl

theorem derivativeNormalizerNDContract_normalizerND
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDContract p row sparse).normalizerND =
      Coeff.symbol "N_D" := rfl

theorem derivativeNormalizerNDContract_normalizedCoefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDContract p row sparse).normalizedCoefficient =
      Coeff.mul (robinGlobalSparseAmplitudeValue p.n sparse row) (Coeff.symbol "N_D_inv") := rfl

/--
Phase-1 source/bound view for the shared `N_D` normalizer contract.

This does not prove the analytic inequality.  It only packages the exact
coefficient source and the paper normalizer symbol used by the future bound
obligation, so `O_DT^S` and `Ry_boundary` can point to the same fixed
interface.
-/
structure DerivativeNormalizerNDSourceBound where
  sourceAnchor : String
  rowValue : Nat
  sparseIndexValue : Nat
  sourceCoefficient : Coeff
  normalizerND : Coeff
  boundFormula : String
  coefficientBound : ObligationRecord
deriving Repr, DecidableEq

/--
Default source/bound interface for the paper statement
`|D_j^(s)| <= N_D`.

The coefficient and obligation are reused from `derivativeNormalizerNDContract`;
the obligation remains false until the coefficient semantics and analytic
normalizer bound are formalized.
-/
def derivativeNormalizerNDSourceBound
    (p : OneTermRobinParameters) (row sparse : Nat) :
    DerivativeNormalizerNDSourceBound :=
  let nd := derivativeNormalizerNDContract p row sparse
  {
    sourceAnchor := nd.sourceAnchor
    rowValue := nd.rowValue
    sparseIndexValue := nd.sparseIndexValue
    sourceCoefficient := nd.coefficient
    normalizerND := nd.normalizerND
    boundFormula := "|D_j^(s)| <= N_D"
    coefficientBound := nd.coefficientBound
  }

theorem derivativeNormalizerNDSourceBound_sourceCoefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDSourceBound p row sparse).sourceCoefficient =
      robinGlobalSparseAmplitudeValue p.n sparse row := rfl

theorem derivativeNormalizerNDSourceBound_normalizerND
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDSourceBound p row sparse).normalizerND =
      Coeff.symbol "N_D" := rfl

theorem derivativeNormalizerNDSourceBound_boundFormula
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDSourceBound p row sparse).boundFormula =
      "|D_j^(s)| <= N_D" := rfl

theorem derivativeNormalizerNDSourceBound_coefficientBound
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDSourceBound p row sparse).coefficientBound =
      (derivativeNormalizerNDContract p row sparse).coefficientBound := rfl

theorem derivativeNormalizerNDSourceBound_coefficientBound_false
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDSourceBound p row sparse).coefficientBound.proved =
      false := rfl

/--
Honest U_indic matrix: controlled-X on the indicator qubit, conditioned on
the system register being in the bulk window [K1, K2].
For each basis state |j⟩:
  - Extract systemVal = bits [1, 1+n) of j
  - If K1 ≤ systemVal ≤ K2 (bulk row): flip indicator bit
  - Otherwise (boundary row): identity
main.tex:1088-1099 --/
def indicatorOracleMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let n := p.n
    let indPos := robinIndicatorBitPosition p
    let systemVal := (j.val >>> 1) &&& ((1 <<< n) - 1)
    let K1 := 2
    let K2 := gridSize n - 3
    let isBulk := if K1 ≤ systemVal ∧ systemVal ≤ K2 then (1 : Nat) else 0
    let expectedImage := j.val ^^^ (isBulk <<< indPos)
    if i.val = expectedImage then Coeff.rat 1 else Coeff.rat 0

/--
Gate matrix for U_indic using the honest permutation matrix.
Controlled-X on indicator bit at position 1+2n, conditioned on bulk membership.
Unitarity proved: indicatorOracleMatrix_is_permutation shows each row and column
has exactly one entry equal to 1, so the matrix is a permutation matrix (hence unitary).
main.tex:1088-1099 --/
def oneTermRobinGate_U_indic (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "U_indic"
  matrix := indicatorOracleMatrix p
  unitary := {
    description := "U_indic(K1,K2) permutation matrix: unitarity proved via indicatorOracleMatrix_is_permutation"
    source := "main.tex:1088-1099"
    proved := true
  }

/--
Theorem-facing Hermitian-conjugate slot for `U_indic`.

The indicator permutation is self-inverse, so its dagger is represented by the
same matrix.  This gate record exists to keep the Fig. 1-term Robin transcript
faithful; the active backend product is still the seven-gate list unless a
separate theorem rewires it.
-/
def oneTermRobinGate_U_indic_dagger (p : OneTermRobinParameters) :
    GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "U_indic^dagger"
  matrix := indicatorOracleMatrix p
  unitary := {
    description := "U_indic^dagger uses the same self-inverse indicator permutation matrix as U_indic"
    source := "GHL2025 Fig. 1-term Robin transcript slot; self-inverse bridge from indicatorOracleImage_self_inverse"
    proved := true
  }

/--
The theorem-facing `U_indic^dagger` slot has the same matrix as `U_indic`.

This is only a transcript bridge.  It does not insert the dagger slot into the
active seven-gate backend product.
-/
theorem oneTermRobinGate_U_indic_dagger_matrix_eq
    (p : OneTermRobinParameters) :
    (oneTermRobinGate_U_indic_dagger p).matrix =
      (oneTermRobinGate_U_indic p).matrix := rfl

/--
Honest O_DT^S diagonal matrix: encodes the sparse amplitude data on the diagonal
for bulk rows (indicator=1) and acts as identity for boundary rows (indicator=0).

For each compound basis state |j⟩:
  - If indicator bit = 0 (boundary row): diagonal entry = Coeff.rat 1 (identity)
  - If indicator bit = 1 (bulk row): diagonal entry = robinSparseAmplitudeValue(n, s, i)
  - Off-diagonal entries are zero.

NOTE: The paper's actual O_{D^T}^S (Lemma 3, main.tex:822-849) is a controlled
rotation on the ancilla qubit, not a diagonal matrix.  This diagonal encoding
exercises the amplitude data pathway; the rotation structure is a proof obligation.
main.tex:822-849 --/
def sparseAmplitudeOracleDTMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    if i.val ≠ j.val then Coeff.rat 0
    else
      let n := p.n
      let indPos := robinIndicatorBitPosition p
      let indBit := (j.val >>> indPos) &&& 1
      if indBit = 0 then
        Coeff.rat 1
      else
        let kappa := p.kappa
        let κbits := clog2 kappa
        let odPure := n - κbits
        let sysMask := (1 <<< n) - 1
        let sysVal := (j.val >>> 1) &&& sysMask
        let sparseStart := 1 + n + odPure
        let sparseMask := (1 <<< κbits) - 1
        let sparseVal := (j.val >>> sparseStart) &&& sparseMask
        robinSparseAmplitudeValue n sparseVal sysVal

/--
Register values used by the faithful Lemma 3 `O_DT^S` contract.

The compound-index convention stores the rotation ancilla in bit 0, the system
row in bits `[1, 1+n)`, the padded sparse register in bits `[1+n, 1+2n)`, and
the indicator bit at `robinIndicatorBitPosition p`.  The `nonAncillaValue`
field is `j >>> 1`; preserving it means that only the ancilla bit may change.
Guseynov-Huang-Liu 2025, Lemma 3, arXiv:2506.20478. -/
structure SparseAmplitudeOracleDTPaperRegisters where
  ancillaBit : Nat
  indicatorBit : Nat
  rowValue : Nat
  sparseIndexValue : Nat
  nonAncillaValue : Nat
deriving Repr, DecidableEq

/--
Extract the Lemma 3 sparse-amplitude oracle registers from a compound basis
index.  This is a source-contract skeleton for the paper's controlled rotation
on the ancilla qubit; it leaves the legacy diagonal data helper available.
-/
def sparseAmplitudeOracleDTPaperRegisters (p : OneTermRobinParameters) (j : Nat) :
    SparseAmplitudeOracleDTPaperRegisters :=
  let n := p.n
  let indPos := robinIndicatorBitPosition p
  let κbits := clog2 p.kappa
  let odPure := n - κbits
  let sysMask := (1 <<< n) - 1
  let sparseStart := 1 + n + odPure
  let sparseMask := (1 <<< κbits) - 1
  {
    ancillaBit := j &&& 1
    indicatorBit := (j >>> indPos) &&& 1
    rowValue := (j >>> 1) &&& sysMask
    sparseIndexValue := (j >>> sparseStart) &&& sparseMask
    nonAncillaValue := j >>> 1
  }

/-- Symbolic cosine half-angle entry for the Lemma 3 O_DT^S rotation. -/
def sparseAmplitudeOracleDTCosHalf (row sparse : Nat) : Coeff :=
  Coeff.symbol s!"odts_cos_half_{row}_{sparse}"

/-- Symbolic sine half-angle entry for the Lemma 3 O_DT^S rotation. -/
def sparseAmplitudeOracleDTSinHalf (row sparse : Nat) : Coeff :=
  Coeff.symbol s!"odts_sin_half_{row}_{sparse}"

/--
Explicit unresolved source obligation for the symbolic entries in the Lemma 3
`O_DT^S` rotation skeleton.

Equation (20) of Guseynov-Huang-Liu 2025 maps `|0>|s>` to an amplitude whose
`|0>` component is `D^(s) / N_D` and whose complementary component is the
square-root normalizer term.  The Lean symbols
`sparseAmplitudeOracleDTCosHalf row sparse` and
`sparseAmplitudeOracleDTSinHalf row sparse` are only placeholders until this
coefficient/normalizer relation and the corresponding two-by-two unitarity
identity are formalized.
-/
def sparseAmplitudeOracleDTCoefficientNormalizerObligation : ObligationRecord := {
  description := "O_DT^S symbolic rotation entries match Eq. (20): D^(s)/N_D amplitude and complementary normalizer term"
  source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
  proved := false
}

/--
Typed Eq. (20) coefficient-normalizer contract for one `O_DT^S` rotation block.

This binds the symbolic rotation entries to the concrete Robin sparse
coefficient data and the paper's `N_D` normalizer without proving the analytic
identities.  The three obligations stay false until Lean has a coefficient
language with the required division, square-root, absolute-value, and unitarity
facts.
-/
structure SparseAmplitudeOracleDTCoefficientNormalizerContract where
  sourceAnchor : String
  rowValue : Nat
  sparseIndexValue : Nat
  coefficient : Coeff
  normalizerND : Coeff
  ketZeroEntry : Coeff
  ketOneEntry : Coeff
  ketZeroFormula : String
  ketOneFormula : String
  coefficientRelation : ObligationRecord
  complementRelation : ObligationRecord
  twoByTwoUnitary : ObligationRecord
deriving Repr, DecidableEq

/--
Default Eq. (20) coefficient-normalizer contract for a Robin row and global
sparse slot. The coefficient is `robinGlobalSparseAmplitudeValue p.n sparse row`; the
rotation entries are the symbols used by `sparseAmplitudeOracleDTRotationMatrix`.
-/
def sparseAmplitudeOracleDTCoefficientNormalizerContract
    (p : OneTermRobinParameters) (row sparse : Nat) :
    SparseAmplitudeOracleDTCoefficientNormalizerContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
  rowValue := row
  sparseIndexValue := sparse
  coefficient := robinGlobalSparseAmplitudeValue p.n sparse row
  normalizerND := Coeff.symbol "N_D"
  ketZeroEntry := sparseAmplitudeOracleDTCosHalf row sparse
  ketOneEntry := sparseAmplitudeOracleDTSinHalf row sparse
  ketZeroFormula := "D_j^(s) / N_D"
  ketOneFormula := "sqrt(1 - |D_j^(s)|^2 / N_D^2)"
  coefficientRelation := {
    description := "ket-zero rotation entry equals D_j^(s) / N_D"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  complementRelation := {
    description := "ket-one rotation entry equals sqrt(1 - |D_j^(s)|^2 / N_D^2)"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }
  twoByTwoUnitary := {
    description := "the Eq. (20) two-by-two ancilla block is unitary under the N_D bound"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), arXiv:2506.20478"
    proved := false
  }

/--
Symbolic stand-in for the Lemma 3 normalized coefficient `D_j^(s) / N_D`.

The factor `Coeff.symbol "N_D_inv"` records the intended division by `N_D`.
It is not a proof that `N_D` is nonzero or that the coefficient lies in the
unit interval required by Eq. (20); those remain separate obligations.
-/
def sparseAmplitudeOracleDTNormalizedCoefficient
    (p : OneTermRobinParameters) (row sparse : Nat) : Coeff :=
  Coeff.mul (robinGlobalSparseAmplitudeValue p.n sparse row) (Coeff.symbol "N_D_inv")

/--
Refined proof route for the `odts_coeff_normalizer` block.

This record separates the typed Eq. (20) data from the analytic obligations:
division by `N_D`, the paper's normalizer bound, the absolute-square term, the
complementary square root, and the two-by-two unitarity identity.  All proof
obligations stay false in Phase 1.
-/
structure SparseAmplitudeOracleDTCoefficientNormalizerProofRoute where
  sourceAnchor : String
  rowValue : Nat
  sparseIndexValue : Nat
  coefficient : Coeff
  normalizerND : Coeff
  normalizedCoefficient : Coeff
  normalizedCoefficientFormula : String
  ketZeroEntry : Coeff
  ketOneEntry : Coeff
  ketZeroFormula : String
  ketOneFormula : String
  coefficientDivision : ObligationRecord
  normalizerBound : ObligationRecord
  absSquareSemantics : ObligationRecord
  sqrtComplementSemantics : ObligationRecord
  twoByTwoUnitary : ObligationRecord
deriving Repr, DecidableEq

/--
Default refined proof route for one `O_DT^S` Eq. (20) coefficient-normalizer
block.  The route keeps the construction fixed to the paper's controlled
rotation and does not promote the gate-level unitarity claim.
-/
def sparseAmplitudeOracleDTCoefficientNormalizerProofRoute
    (p : OneTermRobinParameters) (row sparse : Nat) :
    SparseAmplitudeOracleDTCoefficientNormalizerProofRoute :=
  let c := sparseAmplitudeOracleDTCoefficientNormalizerContract p row sparse
  let nd := derivativeNormalizerNDContract p row sparse
  {
    sourceAnchor := c.sourceAnchor
    rowValue := c.rowValue
    sparseIndexValue := c.sparseIndexValue
    coefficient := c.coefficient
    normalizerND := nd.normalizerND
    normalizedCoefficient := nd.normalizedCoefficient
    normalizedCoefficientFormula := nd.normalizedCoefficientFormula
    ketZeroEntry := c.ketZeroEntry
    ketOneEntry := c.ketOneEntry
    ketZeroFormula := c.ketZeroFormula
    ketOneFormula := c.ketOneFormula
    coefficientDivision := nd.divisionSemantics
    normalizerBound := nd.coefficientBound
    absSquareSemantics := nd.absSquareSemantics
    sqrtComplementSemantics := nd.sqrtComplementSemantics
    twoByTwoUnitary := c.twoByTwoUnitary
  }

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_coefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
      (sparseAmplitudeOracleDTCoefficientNormalizerContract p row sparse).coefficient := rfl

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_normalizerND
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerND =
      (sparseAmplitudeOracleDTCoefficientNormalizerContract p row sparse).normalizerND := rfl

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_normalizedCoefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizedCoefficient =
      sparseAmplitudeOracleDTNormalizedCoefficient p row sparse := rfl

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_sharedND
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound =
      (derivativeNormalizerNDContract p row sparse).coefficientBound ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficientDivision =
      (derivativeNormalizerNDContract p row sparse).divisionSemantics ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).absSquareSemantics =
      (derivativeNormalizerNDContract p row sparse).absSquareSemantics ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).sqrtComplementSemantics =
      (derivativeNormalizerNDContract p row sparse).sqrtComplementSemantics := by
  exact ⟨rfl, rfl, rfl, rfl⟩

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_sourceBound
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
      (derivativeNormalizerNDSourceBound p row sparse).sourceCoefficient ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerND =
      (derivativeNormalizerNDSourceBound p row sparse).normalizerND ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound =
      (derivativeNormalizerNDSourceBound p row sparse).coefficientBound := by
  exact ⟨rfl, rfl, rfl⟩

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_ketZeroEntry
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).ketZeroEntry =
      (sparseAmplitudeOracleDTCoefficientNormalizerContract p row sparse).ketZeroEntry := rfl

theorem sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_ketOneEntry
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).ketOneEntry =
      (sparseAmplitudeOracleDTCoefficientNormalizerContract p row sparse).ketOneEntry := rfl

/--
Faithful Lemma 3 controlled-rotation skeleton for `O_DT^S`.

For columns whose indicator bit is 0, the matrix acts as identity.  For columns
whose indicator bit is 1, it preserves every non-ancilla bit and applies a
symbolic two-by-two rotation on ancilla bit 0.  The symbols are indexed by the
extracted row and sparse-index values; their connection to the Eq. (20)
amplitudes determined by `robinGlobalSparseAmplitudeValue p.n sparse row / N_D`
remains the coefficient-normalizer proof obligation.
Guseynov-Huang-Liu 2025, Lemma 3, arXiv:2506.20478. -/
def sparseAmplitudeOracleDTRotationMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let regs := sparseAmplitudeOracleDTPaperRegisters p j.val
    if regs.indicatorBit = 0 then
      if i.val = j.val then Coeff.rat 1 else Coeff.rat 0
    else if i.val >>> 1 ≠ regs.nonAncillaValue then
      Coeff.rat 0
    else
      let cosHalf := sparseAmplitudeOracleDTCosHalf regs.rowValue regs.sparseIndexValue
      let sinHalf := sparseAmplitudeOracleDTSinHalf regs.rowValue regs.sparseIndexValue
      let anc_i := i.val &&& 1
      match regs.ancillaBit, anc_i with
      | 0, 0 => cosHalf
      | 0, 1 => sinHalf
      | 1, 0 => Coeff.neg sinHalf
      | _, _ => cosHalf

/--
Gate matrix for O_DT^S using the faithful controlled-rotation skeleton.
The legacy diagonal helper `sparseAmplitudeOracleDTMatrix` remains available as
the coefficient-data path, but the active gate now preserves all non-ancilla
bits and rotates bit 0 when the indicator bit is 1.  Unitarity and the
normalizer-bound trigonometric identity are not yet formally proved.
main.tex:822-849 --/
def oneTermRobinGate_O_DT_S (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "O_DT^S"
  matrix := sparseAmplitudeOracleDTRotationMatrix p
  unitary := {
    description := "O_DT^S controlled-rotation skeleton on ancilla bit: unitarity and normalizer bound not yet proved"
    source := "Guseynov-Huang-Liu 2025, Lemma 3, arXiv:2506.20478"
    proved := false
  }

/--
Register values used by the faithful `Ry_boundary` source contract.

The compound-index convention is the same one used by the active matrix:
ancilla bit 0 is the rotated qubit, bits `[1, 1+n)` contain the Robin row,
the high part of the O_D register contains sparse index `s`, and the indicator
bit determines whether the boundary rotation is active.  The `nonAncillaValue`
field is preserved by the controlled rotation.
Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Eq. angles for Ry,
arXiv:2506.20478. -/
structure BoundaryRotationPaperRegisters where
  ancillaBit : Nat
  indicatorBit : Nat
  rowValue : Nat
  sparseIndexValue : Nat
  nonAncillaValue : Nat
deriving Repr, DecidableEq

/--
Extract the `Ry_boundary` register fields from a compound basis index.
This is a source-contract skeleton; it does not prove the angle identities or
unitarity of the symbolic rotation block.
-/
def boundaryRotationPaperRegisters (p : OneTermRobinParameters) (j : Nat) :
    BoundaryRotationPaperRegisters :=
  let n := p.n
  let indPos := robinIndicatorBitPosition p
  let κbits := clog2 p.kappa
  let odPure := n - κbits
  let sysMask := (1 <<< n) - 1
  let sparseStart := 1 + n + odPure
  let sparseMask := (1 <<< κbits) - 1
  {
    ancillaBit := j &&& 1
    indicatorBit := (j >>> indPos) &&& 1
    rowValue := (j >>> 1) &&& sysMask
    sparseIndexValue := (j >>> sparseStart) &&& sparseMask
    nonAncillaValue := j >>> 1
  }

/-- Symbolic cosine half-angle entry for the `Ry_boundary` rotation. -/
def boundaryRotationCosHalf (row sparse : Nat) : Coeff :=
  Coeff.symbol s!"boundary_cos_half_{row}_{sparse}"

/-- Symbolic sine half-angle entry for the `Ry_boundary` rotation. -/
def boundaryRotationSinHalf (row sparse : Nat) : Coeff :=
  Coeff.symbol s!"boundary_sin_half_{row}_{sparse}"

/--
Explicit unresolved source obligation for the `Ry_boundary` angle/normalizer
relation.

The paper uses angles `theta_j^s = arccos(D_j^(s) / N_D)` for boundary rows.
The Lean symbols `boundaryRotationCosHalf row sparse` and
`boundaryRotationSinHalf row sparse` are placeholders until the half-angle
identities and the two-by-two unitarity relation are formalized.
-/
def boundaryRotationAngleNormalizerObligation : ObligationRecord := {
  description := "Ry_boundary symbolic entries match theta_j^s = arccos(D_j^(s) / N_D) and the half-angle formulas"
  source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Eq. angles for Ry, arXiv:2506.20478"
  proved := false
}

/--
Typed angle/normalizer contract for one `Ry_boundary` rotation block.

This binds the symbolic half-angle entries used by `boundaryRotationMatrix` to
the Robin sparse coefficient source and the paper normalizer `N_D`.  It records
the exact obligations without asserting the arccos relation, half-angle
formulas, control condition, or unitarity.
-/
structure BoundaryRotationAngleNormalizerContract where
  sourceAnchor : String
  rowValue : Nat
  sparseIndexValue : Nat
  coefficient : Coeff
  normalizerND : Coeff
  thetaFormula : String
  cosHalfEntry : Coeff
  sinHalfEntry : Coeff
  cosHalfFormula : String
  sinHalfFormula : String
  boundaryControl : ObligationRecord
  arccosArgumentRelation : ObligationRecord
  cosHalfRelation : ObligationRecord
  sinHalfRelation : ObligationRecord
  twoByTwoUnitary : ObligationRecord
deriving Repr, DecidableEq

/--
Default `Ry_boundary` angle/normalizer contract for one Robin row and global
sparse slot. The coefficient is `robinGlobalSparseAmplitudeValue p.n sparse row`; the
rotation entries are the symbols used by `boundaryRotationMatrix`.
-/
def boundaryRotationAngleNormalizerContract
    (p : OneTermRobinParameters) (row sparse : Nat) :
    BoundaryRotationAngleNormalizerContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Eq. angles for Ry, arXiv:2506.20478"
  rowValue := row
  sparseIndexValue := sparse
  coefficient := robinGlobalSparseAmplitudeValue p.n sparse row
  normalizerND := Coeff.symbol "N_D"
  thetaFormula := "theta_j^s = arccos(D_j^(s) / N_D)"
  cosHalfEntry := boundaryRotationCosHalf row sparse
  sinHalfEntry := boundaryRotationSinHalf row sparse
  cosHalfFormula := "sqrt((1 + D_j^(s) / N_D) / 2)"
  sinHalfFormula := "sqrt((1 - D_j^(s) / N_D) / 2)"
  boundaryControl := {
    description := "Ry_boundary acts only on boundary rows selected by indicator bit 0"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin, arXiv:2506.20478"
    proved := false
  }
  arccosArgumentRelation := {
    description := "theta_j^s is arccos(D_j^(s) / N_D) for the recorded Robin coefficient; blocked until Coeff has division and real arccos semantics"
    source := "Guseynov-Huang-Liu 2025, Eq. angles for Ry, arXiv:2506.20478"
    proved := false
  }
  cosHalfRelation := {
    description := "cos(theta_j^s / 2) equals sqrt((1 + D_j^(s) / N_D) / 2); blocked until Coeff has square-root and half-angle semantics"
    source := "Guseynov-Huang-Liu 2025, Eq. angles for Ry, arXiv:2506.20478"
    proved := false
  }
  sinHalfRelation := {
    description := "sin(theta_j^s / 2) equals sqrt((1 - D_j^(s) / N_D) / 2); blocked until Coeff has square-root and half-angle semantics"
    source := "Guseynov-Huang-Liu 2025, Eq. angles for Ry, arXiv:2506.20478"
    proved := false
  }
  twoByTwoUnitary := {
    description := "the Ry_boundary two-by-two block is unitary under the N_D bound"
    source := "Guseynov-Huang-Liu 2025, Eq. angles for Ry, arXiv:2506.20478"
    proved := false
  }

/--
The coefficient source of the `Ry_boundary` angle contract is definitionally
the Robin global sparse-slot amplitude data layer.
-/
theorem boundaryRotationAngleNormalizerContract_coefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (boundaryRotationAngleNormalizerContract p row sparse).coefficient =
      robinGlobalSparseAmplitudeValue p.n sparse row := rfl

/--
Symbolic stand-in for the paper argument `D_j^(s) / N_D`.

The factor `Coeff.symbol "N_D_inv"` is not a proof that `N_D` is invertible.
It only records the intended normalized coefficient while the required division
semantics and nonzero normalizer condition remain explicit obligations.
-/
def boundaryRotationNormalizedCoefficient
    (p : OneTermRobinParameters) (row sparse : Nat) : Coeff :=
  Coeff.mul (robinGlobalSparseAmplitudeValue p.n sparse row) (Coeff.symbol "N_D_inv")

/--
Refined proof route for the `ryb_angle_normalizer` block.

This record separates the typed data already present in
`BoundaryRotationAngleNormalizerContract` from the missing analytic semantics:
division by `N_D`, real arccos, square roots, the paper's normalizer bound, and
the resulting two-by-two unitarity identity.  All proof obligations stay false
in Phase 1.
-/
structure BoundaryRotationAngleNormalizerProofRoute where
  sourceAnchor : String
  rowValue : Nat
  sparseIndexValue : Nat
  coefficient : Coeff
  normalizerND : Coeff
  arccosArgument : Coeff
  arccosArgumentFormula : String
  thetaFormula : String
  cosHalfEntry : Coeff
  sinHalfEntry : Coeff
  cosHalfFormula : String
  sinHalfFormula : String
  coefficientDivision : ObligationRecord
  realArccosSemantics : ObligationRecord
  halfAngleSemantics : ObligationRecord
  normalizerBound : ObligationRecord
  twoByTwoUnitary : ObligationRecord
deriving Repr, DecidableEq

/--
Default refined proof route for one `Ry_boundary` angle-normalizer block.

The route keeps the construction fixed to the paper formula
`theta_j^s = arccos(D_j^(s) / N_D)`.  It does not introduce a replacement angle
or promote the gate-level unitarity claim.
-/
def boundaryRotationAngleNormalizerProofRoute
    (p : OneTermRobinParameters) (row sparse : Nat) :
    BoundaryRotationAngleNormalizerProofRoute :=
  let c := boundaryRotationAngleNormalizerContract p row sparse
  let nd := derivativeNormalizerNDContract p row sparse
  {
    sourceAnchor := c.sourceAnchor
    rowValue := c.rowValue
    sparseIndexValue := c.sparseIndexValue
    coefficient := c.coefficient
    normalizerND := nd.normalizerND
    arccosArgument := nd.normalizedCoefficient
    arccosArgumentFormula := nd.normalizedCoefficientFormula
    thetaFormula := c.thetaFormula
    cosHalfEntry := c.cosHalfEntry
    sinHalfEntry := c.sinHalfEntry
    cosHalfFormula := c.cosHalfFormula
    sinHalfFormula := c.sinHalfFormula
    coefficientDivision := nd.divisionSemantics
    realArccosSemantics := nd.arccosSemantics
    halfAngleSemantics := {
      description := "derive the displayed cosine and sine half-angle formulas from theta_j^s"
      source := "Guseynov-Huang-Liu 2025, Eq. angles for Ry, arXiv:2506.20478"
      proved := false
    }
    normalizerBound := nd.coefficientBound
    twoByTwoUnitary := c.twoByTwoUnitary
  }

theorem boundaryRotationAngleNormalizerProofRoute_coefficient
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient =
      (boundaryRotationAngleNormalizerContract p row sparse).coefficient := rfl

theorem boundaryRotationAngleNormalizerProofRoute_arccosArgument
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (boundaryRotationAngleNormalizerProofRoute p row sparse).arccosArgument =
      boundaryRotationNormalizedCoefficient p row sparse := rfl

theorem boundaryRotationAngleNormalizerProofRoute_sharedND
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound =
      (derivativeNormalizerNDContract p row sparse).coefficientBound ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficientDivision =
      (derivativeNormalizerNDContract p row sparse).divisionSemantics ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).realArccosSemantics =
      (derivativeNormalizerNDContract p row sparse).arccosSemantics := by
  exact ⟨rfl, rfl, rfl⟩

theorem boundaryRotationAngleNormalizerProofRoute_sourceBound
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient =
      (derivativeNormalizerNDSourceBound p row sparse).sourceCoefficient ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerND =
      (derivativeNormalizerNDSourceBound p row sparse).normalizerND ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound =
      (derivativeNormalizerNDSourceBound p row sparse).coefficientBound := by
  exact ⟨rfl, rfl, rfl⟩

theorem derivativeNormalizerNDSourceBound_sharedRoutes
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
      (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerND =
      (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerND ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound =
      (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound := by
  exact ⟨rfl, rfl, rfl⟩

/--
Bridge showing that the shared `N_D` route is now sourced from the active
global sparse-slot coefficient table.

This only wires coefficient data through the existing contracts. It does not
prove the analytic division, arccos, half-angle, or unitarity obligations.
-/
theorem robinGlobalSparseAmplitudeValue_sharedNormalizerRoutes
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDSourceBound p row sparse).sourceCoefficient =
      robinGlobalSparseAmplitudeValue p.n sparse row ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
      robinGlobalSparseAmplitudeValue p.n sparse row ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient =
      robinGlobalSparseAmplitudeValue p.n sparse row ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
      (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/--
Honest Ry_boundary matrix: controlled R_y rotation on the ancilla qubit (bit 0),
conditioned on the indicator bit being 0 (boundary row).

For bulk rows (indicator=1): acts as identity (no rotation).
For boundary rows (indicator=0): applies R_y(θ_j^s) on the ancilla qubit,
where θ_j^s = arccos(D_j^(s) / N_D) (main.tex:1115-1120, Eq. angles for Ry).

The R_y(θ) matrix on the ancilla qubit:
  M(|0⟩, |0⟩) = cos(θ/2),  M(|1⟩, |0⟩) = sin(θ/2)
  M(|0⟩, |1⟩) = -sin(θ/2), M(|1⟩, |1⟩) = cos(θ/2)

Rotation entries are symbolic since the exact trigonometric values involve
square roots: cos(θ/2) = √((1 + D/N_D)/2), sin(θ/2) = √((1 - D/N_D)/2).
main.tex:1115-1120 --/
def boundaryRotationMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let n := p.n
    let indPos := robinIndicatorBitPosition p
    let indBit_j := (j.val >>> indPos) &&& 1
    if indBit_j = 1 then
      if i.val = j.val then Coeff.rat 1 else Coeff.rat 0
    else
      let anc_j := j.val &&& 1
      let anc_i := i.val &&& 1
      if i.val >>> 1 ≠ j.val >>> 1 then Coeff.rat 0
      else
        let kappa := p.kappa
        let κbits := clog2 kappa
        let odPure := n - κbits
        let sysMask := (1 <<< n) - 1
        let sysVal := (j.val >>> 1) &&& sysMask
        let sparseStart := 1 + n + odPure
        let sparseMask := (1 <<< κbits) - 1
        let sparseVal := (j.val >>> sparseStart) &&& sparseMask
        let cosHalf := boundaryRotationCosHalf sysVal sparseVal
        let sinHalf := boundaryRotationSinHalf sysVal sparseVal
        match anc_j, anc_i with
        | 0, 0 => cosHalf
        | 0, 1 => sinHalf
        | 1, 0 => Coeff.neg sinHalf
        | _, _ => cosHalf

/--
Gate matrix for Ry_boundary using the honest controlled rotation matrix.
R_y rotation on the ancilla qubit for boundary rows (indicator=0);
identity for bulk rows (indicator=1).
Unitarity not yet formally proved.
main.tex:1115-1120 --/
def oneTermRobinGate_Ry_boundary (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "Ry_boundary"
  matrix := boundaryRotationMatrix p
  unitary := {
    description := "Ry_boundary honest controlled rotation matrix: unitarity not yet proved"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Eq. angles for Ry, arXiv:2506.20478"
    proved := false
  }

/--
Guard for the shared `N_D` Phase-1 route.

The source-bound bridges only synchronize the two proof routes.  This theorem
records that the analytic obligations and the two affected gate unitarity
flags still have not been promoted.
Guseynov-Huang-Liu 2025, Lemma 3, Eq. (20), and Eq. angles for Ry,
arXiv:2506.20478.
-/
theorem derivativeNormalizerNDSharedRoute_flags_false
    (p : OneTermRobinParameters) (row sparse : Nat) :
    (derivativeNormalizerNDContract p row sparse).nonzeroNormalizer.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).divisionSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).coefficientBound.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).absSquareSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).sqrtComplementSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).arccosSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).twoByTwoUnitary.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficientDivision.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).absSquareSemantics.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).sqrtComplementSemantics.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).twoByTwoUnitary.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficientDivision.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).realArccosSemantics.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).halfAngleSemantics.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).twoByTwoUnitary.proved = false ∧
    (oneTermRobinGate_O_DT_S p).unitary.proved = false ∧
    (oneTermRobinGate_Ry_boundary p).unitary.proved = false := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl,
    rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/--
Combined Phase-1 guard for the shared `N_D` route.

This packages the source-bound bridges for `O_DT^S` and `Ry_boundary` together
with the current false-flag state.  It is bookkeeping only: the analytic
division, bound, square-root, arccos, half-angle, and unitarity obligations are
still unproved.
-/
theorem derivativeNormalizerNDSharedRoute_sourceBoundAndFlags
    (p : OneTermRobinParameters) (row sparse : Nat) :
    ((sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
        (derivativeNormalizerNDSourceBound p row sparse).sourceCoefficient ∧
      (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerND =
        (derivativeNormalizerNDSourceBound p row sparse).normalizerND ∧
      (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound =
        (derivativeNormalizerNDSourceBound p row sparse).coefficientBound) ∧
    ((boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient =
        (derivativeNormalizerNDSourceBound p row sparse).sourceCoefficient ∧
      (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerND =
        (derivativeNormalizerNDSourceBound p row sparse).normalizerND ∧
      (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound =
        (derivativeNormalizerNDSourceBound p row sparse).coefficientBound) ∧
    ((sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficient =
        (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficient ∧
      (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerND =
        (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerND ∧
      (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound =
        (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound) ∧
    (derivativeNormalizerNDContract p row sparse).nonzeroNormalizer.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).divisionSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).coefficientBound.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).absSquareSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).sqrtComplementSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).arccosSemantics.proved = false ∧
    (derivativeNormalizerNDContract p row sparse).twoByTwoUnitary.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).coefficientDivision.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).normalizerBound.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).absSquareSemantics.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).sqrtComplementSemantics.proved = false ∧
    (sparseAmplitudeOracleDTCoefficientNormalizerProofRoute p row sparse).twoByTwoUnitary.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).coefficientDivision.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).realArccosSemantics.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).halfAngleSemantics.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).normalizerBound.proved = false ∧
    (boundaryRotationAngleNormalizerProofRoute p row sparse).twoByTwoUnitary.proved = false ∧
    (oneTermRobinGate_O_DT_S p).unitary.proved = false ∧
    (oneTermRobinGate_Ry_boundary p).unitary.proved = false := by
  exact ⟨
    sparseAmplitudeOracleDTCoefficientNormalizerProofRoute_sourceBound p row sparse,
    boundaryRotationAngleNormalizerProofRoute_sourceBound p row sparse,
    derivativeNormalizerNDSourceBound_sharedRoutes p row sparse,
    derivativeNormalizerNDSharedRoute_flags_false p row sparse⟩

/--
Interim O_D^BS column-map helper, not the faithful Lemma 1 paper oracle.
It maps |s⟩|i⟩ → |s⟩|col(s,i)⟩ by replacing the system register bits.
Bits outside the system register are preserved.  The paper contract
|0>^(n-l)|s>^l|i>^n -> |r_si>^n|i>^n is recorded separately in
`defaultBandedSparseAccessPaperContract`; do not use this helper as the
unitarity or block-extraction target for the paper oracle.
main.tex:784-801 --/
def bandedSparseAccessMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let n := p.n
    let kappa := p.kappa
    let κbits := clog2 kappa
    let odPure := n - κbits
    let sysMask := (1 <<< n) - 1
    let sysVal := (j.val >>> 1) &&& sysMask
    let sparseStart := 1 + n + odPure
    let sparseMask := (1 <<< κbits) - 1
    let sparseVal := (j.val >>> sparseStart) &&& sparseMask
    let col := robinSparseColumnMap n sparseVal sysVal
    let expectedImage := j.val - (j.val &&& (sysMask <<< 1)) + (col <<< 1)
    if i.val = expectedImage then Coeff.rat 1 else Coeff.rat 0

/--
Gate record for the faithful Lemma 1 O_D^BS paper-image matrix skeleton.

The matrix uses `bandedSparseAccessPaperMatrix`, which preserves the row
register and writes `r_si` into the padded sparse-address register.  Unitarity,
forward correctness, and block extraction remain unproved obligations.
Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478. -/
def oneTermRobinGate_O_D_BS (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "O_D^BS"
  matrix := bandedSparseAccessPaperMatrix p
  unitary := {
    description := "O_D^BS paper-image matrix skeleton: unitarity and cleanup not yet proved"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- Active forward `O_D^BS` gate entry at the finite paper image. -/
theorem oneTermRobinGate_O_D_BS_imageFin_eq_one
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    (oneTermRobinGate_O_D_BS p).matrix
        (bandedSparseAccessPaperImageFin p j haddr) j =
      Coeff.rat 1 := by
  simpa [oneTermRobinGate_O_D_BS]
    using bandedSparseAccessPaperMatrix_imageFin_eq_one p j haddr

/--
Concrete contract-drift guard separating the active Lemma 1 paper-image matrix
from the legacy sparse-column helper.

For the one-term parameters `n = 3`, `kappa = 7`, source column `8` is sent by
the paper-image skeleton to row `40`.  The active `O_D^BS` gate therefore has
entry `(40, 8) = 1` and no entry at `(4, 8)`, while the legacy helper still has
its historical row-`4` entry.  This is only a regression guard; it does not
promote unitarity, cleanup, or block extraction.
-/
theorem oneTermRobinGate_O_D_BS_contractDrift_column8_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperImage p 8 = 40 ∧
      (oneTermRobinGate_O_D_BS p).matrix
          ⟨40, by native_decide⟩ ⟨8, by native_decide⟩ = Coeff.rat 1 ∧
      (oneTermRobinGate_O_D_BS p).matrix
          ⟨4, by native_decide⟩ ⟨8, by native_decide⟩ = Coeff.rat 0 ∧
      (bandedSparseAccessMatrix p)
          ⟨4, by native_decide⟩ ⟨8, by native_decide⟩ = Coeff.rat 1 ∧
      (oneTermRobinGate_O_D_BS p).unitary.proved = false := by
  native_decide

/--
Concrete rejected-model collision for the old row-dependent `O_D^BS` address.

For the one-term parameters `n = 3`, `kappa = 7`, boundary row `0` has only
three nonzero Robin stencil entries.  The old row-dependent address folded
sparse index `3` back to the row address, colliding with sparse index `0`.
The active global-slot paper image separates these columns; this theorem is
retained only as regression memory for the rejected address model.
-/
theorem oneTermRobinGate_O_D_BS_boundaryUnusedSparseCollision_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperCleanInput p 0 = true ∧
      bandedSparseAccessPaperCleanInput p 48 = true ∧
      (bandedSparseAccessPaperRegisters p 0).rowValue = 0 ∧
      (bandedSparseAccessPaperRegisters p 48).rowValue = 0 ∧
      (bandedSparseAccessPaperRegisters p 0).sparseIndexValue = 0 ∧
      (bandedSparseAccessPaperRegisters p 48).sparseIndexValue = 3 ∧
      bandedSparseAccessRowDependentPaperAddress p 0 = 0 ∧
      bandedSparseAccessRowDependentPaperAddress p 48 = 0 ∧
      bandedSparseAccessRowDependentPaperImage p 0 =
        bandedSparseAccessRowDependentPaperImage p 48 ∧
      bandedSparseAccessPaperAddress p 0 = 6 ∧
      bandedSparseAccessPaperAddress p 48 = 1 ∧
      bandedSparseAccessPaperImage p 0 ≠ bandedSparseAccessPaperImage p 48 ∧
      0 ≠ 48 := by
  native_decide

/--
Concrete regression that the corrected active global-slot image separates the
old boundary unused-sparse collision columns.

No semantic proof flag is promoted: this only checks the active image entries
for the two concrete clean columns.
-/
theorem oneTermRobinGate_O_D_BS_globalSparseBoundaryNoCollision_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperCleanInput p 0 = true ∧
      bandedSparseAccessPaperCleanInput p 48 = true ∧
      bandedSparseAccessPaperAddress p 0 = 6 ∧
      bandedSparseAccessPaperAddress p 48 = 1 ∧
      bandedSparseAccessPaperImage p 0 = 96 ∧
      bandedSparseAccessPaperImage p 48 = 16 ∧
      bandedSparseAccessPaperImage p 0 ≠ bandedSparseAccessPaperImage p 48 ∧
      (oneTermRobinGate_O_D_BS p).matrix
          ⟨96, by native_decide⟩ ⟨0, by native_decide⟩ = Coeff.rat 1 ∧
      (oneTermRobinGate_O_D_BS p).matrix
          ⟨16, by native_decide⟩ ⟨48, by native_decide⟩ = Coeff.rat 1 ∧
      (oneTermRobinGate_O_D_BS p).unitary.proved = false := by
  native_decide

/--
The old boundary collision columns are both in the faithful global-slot source
domain even though one of them is outside the rejected row-dependent
nonzero-branch classifier.

This is the regression that prevents future lower packets from treating
`bandedSparseAccessPaperValidCleanSource` as the active source predicate.
-/
theorem bandedSparseAccessPaperGlobalSlotSource_boundaryColumns_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperGlobalSlotSource p 0 = true ∧
      bandedSparseAccessPaperGlobalSlotSource p 48 = true ∧
      bandedSparseAccessPaperValidCleanSource p 48 = false ∧
      bandedSparseAccessPaperImage p 0 ≠ bandedSparseAccessPaperImage p 48 ∧
      (oneTermRobinGate_O_D_BS p).unitary.proved = false := by
  native_decide

/--
Encoded sparse value `7` is the first out-of-range slot for the one-term
`kappa = 7` contract.  It is clean in the padded O_D register but not in the
faithful global-slot source domain.
-/
theorem bandedSparseAccessPaperGlobalSlotSource_encodedOutOfRange_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    bandedSparseAccessPaperCleanInput p 112 = true ∧
      (bandedSparseAccessPaperRegisters p 112).sparseIndexValue = 7 ∧
      bandedSparseAccessPaperSparseIndexInKappa p 112 = false ∧
      bandedSparseAccessPaperGlobalSlotSource p 112 = false ∧
      (oneTermRobinGate_O_D_BS p).unitary.proved = false := by
  native_decide

/--
Symbolic function value at grid point j.
Returns Coeff.symbol "f_x_j" for each grid index.
The paper's O_f (Theorem amplitude-oracle for piece-wise polynomial function,
main.tex:870-910) encodes f(x_j)/N_f;
the 1/N_f factor is absorbed into the normalizer α = N_D · N_f · κ.
main.tex:870-910 --/
def robinFunctionValue (n i : Nat) : Coeff :=
  Coeff.symbol s!"f_{n}_{i}"

/--
Register values used by the paper-level function oracle `O_f` contract.

The compound-index convention stores the system row in bits `[1, 1+n)` and
stores the `m_f` function-oracle workspace immediately above the indicator bit,
starting at `robinIndicatorBitPosition p + 1`.  This record is a source-contract
skeleton for the paper's clean-workspace equation; it does not assert the
amplitude relation or workspace cleanup.
Guseynov-Huang-Liu 2025, function-oracle construction, arXiv:2506.20478. -/
structure FunctionOraclePaperRegisters where
  systemValue : Nat
  mfWorkspaceValue : Nat
  nonMFValue : Nat
  cleanWorkspace : Bool
deriving Repr, DecidableEq

/--
Extract the system register and the `m_f` function workspace from a compound
basis index for the `O_f` source contract.

The `nonMFValue` field is the input index with the `m_f` workspace bits cleared.
For clean-workspace columns this is the clean-branch basis index appearing in
the paper equation.
-/
def functionOraclePaperRegisters (p : OneTermRobinParameters) (j : Nat) :
    FunctionOraclePaperRegisters :=
  let n := p.n
  let rp := defaultRobinRegisterPartition p
  let sysMask := (1 <<< n) - 1
  let mfStart := robinIndicatorBitPosition p + 1
  let mfMask := (1 <<< rp.mfQubits) - 1
  let mfValue := (j >>> mfStart) &&& mfMask
  {
    systemValue := (j >>> 1) &&& sysMask
    mfWorkspaceValue := mfValue
    nonMFValue := j - (j &&& (mfMask <<< mfStart))
    cleanWorkspace := mfValue == 0
  }

/--
Symbolic normalized clean-branch amplitude for the paper's function oracle.

The reciprocal symbol records the intended factor `1 / N_f` without proving
that `N_f` is nonzero or that the amplitude is bounded.
-/
def functionOracleNormalizedValue (p : OneTermRobinParameters) (i : Nat) : Coeff :=
  Coeff.mul (robinFunctionValue p.n i) (Coeff.symbol "N_f_inv")

/--
Paper-image source contract for one column of the function oracle `O_f`.

The clean branch records the displayed paper component
`(f(x_i)/N_f)|0>^mf|i>`.  The orthogonal component and all analytic side
conditions are tracked as false obligations; this record is not a matrix proof
and does not promote the current diagonal helper to a faithful oracle.
-/
structure FunctionOraclePaperImage where
  sourceAnchor : String
  inputRegisters : FunctionOraclePaperRegisters
  cleanBranchBasisIndex : Nat
  cleanBranchSystemValue : Nat
  cleanBranchWorkspaceValue : Nat
  cleanBranchAmplitude : Coeff
  orthogonalComponent : String
  systemPreserved : Bool
  cleanWorkspaceBranch : Bool
  normalizedAmplitudeCorrect : ObligationRecord
  orthogonalComponentCorrect : ObligationRecord
  normalizerBound : ObligationRecord
  unitaryCompletion : ObligationRecord
  diagonalHelperIsolation : ObligationRecord
deriving Repr, DecidableEq

/--
Build the paper-level `O_f` image contract for one compound basis column.

This captures the register-level target
`|0>^mf|i> ↦ (f(x_i)/N_f)|0>^mf|i> + |orth_f(i)>` as data and keeps every
unproved semantic claim explicit.
-/
def functionOraclePaperImage (p : OneTermRobinParameters) (j : Nat) :
    FunctionOraclePaperImage :=
  let regs := functionOraclePaperRegisters p j
  {
    sourceAnchor := "Guseynov-Huang-Liu 2025, function oracle O_f, arXiv:2506.20478"
    inputRegisters := regs
    cleanBranchBasisIndex := regs.nonMFValue
    cleanBranchSystemValue := regs.systemValue
    cleanBranchWorkspaceValue := 0
    cleanBranchAmplitude := functionOracleNormalizedValue p regs.systemValue
    orthogonalComponent := s!"orth_f_{p.n}_{regs.systemValue}"
    systemPreserved := regs.systemValue == ((regs.nonMFValue >>> 1) &&& ((1 <<< p.n) - 1))
    cleanWorkspaceBranch := regs.cleanWorkspace
    normalizedAmplitudeCorrect := {
      description := "clean O_f branch amplitude equals f(x_i) / N_f"
      source := "Guseynov-Huang-Liu 2025, function oracle O_f, arXiv:2506.20478"
      proved := false
    }
    orthogonalComponentCorrect := {
      description := "O_f orthogonal component has zero overlap with the clean m_f workspace branch and preserves the system label"
      source := "Guseynov-Huang-Liu 2025, function oracle O_f, arXiv:2506.20478"
      proved := false
    }
    normalizerBound := {
      description := "N_f bounds the coefficient-function amplitudes used by O_f"
      source := "Guseynov-Huang-Liu 2025, function oracle O_f, arXiv:2506.20478"
      proved := false
    }
    unitaryCompletion := {
      description := "O_f paper image extends to a unitary with the recorded orthogonal component"
      source := "Guseynov-Huang-Liu 2025, function oracle O_f, arXiv:2506.20478"
      proved := false
    }
    diagonalHelperIsolation := {
      description := "functionOracleMatrix is helper-only until the paper O_f image is wired to a full matrix"
      source := "QBE-AUTO-002 O_f source-contract audit"
      proved := false
    }
  }

/-- Bridge lemma: the `O_f` paper image uses the shared register extractor. -/
theorem functionOraclePaperImage_inputRegisters_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOraclePaperImage p j).inputRegisters =
      functionOraclePaperRegisters p j := rfl

/-- Bridge lemma: the clean `O_f` branch clears only the `m_f` workspace bits. -/
theorem functionOraclePaperImage_cleanBranchBasisIndex_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOraclePaperImage p j).cleanBranchBasisIndex =
      (functionOraclePaperRegisters p j).nonMFValue := rfl

/-- Bridge lemma: the clean `O_f` branch preserves the extracted system value. -/
theorem functionOraclePaperImage_cleanBranchSystemValue_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOraclePaperImage p j).cleanBranchSystemValue =
      (functionOraclePaperRegisters p j).systemValue := rfl

/-- Bridge lemma: the clean `O_f` branch has zero `m_f` workspace value. -/
theorem functionOraclePaperImage_cleanBranchWorkspaceValue_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOraclePaperImage p j).cleanBranchWorkspaceValue = 0 := rfl

/--
Bridge lemma: the clean `O_f` branch amplitude is the normalized function value
at the system value extracted from the same column.
-/
theorem functionOraclePaperImage_cleanBranchAmplitude_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOraclePaperImage p j).cleanBranchAmplitude =
      functionOracleNormalizedValue p (functionOraclePaperRegisters p j).systemValue := rfl

/-- Bridge lemma: the clean-workspace branch flag is inherited from the extractor. -/
theorem functionOraclePaperImage_cleanWorkspaceBranch_eq
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOraclePaperImage p j).cleanWorkspaceBranch =
      (functionOraclePaperRegisters p j).cleanWorkspace := rfl

/--
External source transcript for the O_f amplitude-oracle theorem cited by
GHL2025.

This records the theorem and coordinate-oracle equation used as a source
contract for the function oracle.  It does not formalize the cited theorem and
does not close the analytic facts needed for the Lean `O_f` contract.
-/
structure FunctionOracleExternalAmplitudeSourceContract where
  sourceAnchor : String
  theoremAnchor : String
  coordinateOracleAnchor : String
  citedSourceAnchor : String
  cleanBranchFormula : String
  normalizerNf : Coeff
  resourceClaim : ObligationRecord
  externalTheoremFormalized : ObligationRecord
  nonzeroNormalizer : ObligationRecord
  divisionSemantics : ObligationRecord
  theoremAmplitudeCorrect : ObligationRecord
  closesNormalizerBound : Bool
  closesOrthogonalCompletion : Bool
  closesUnitaryCompletion : Bool
  closesFunctionOracleContract : Bool
deriving Repr, DecidableEq

/--
Default source transcript for GHL2025's function-oracle dependency.

The GHL2025 theorem cites Guseynov--Liu 2024, arXiv:2411.01131, Theorem 5.
The QBE status remains obligation-only: this declaration gives later proof
packets a typed source anchor, not a proof of the theorem.
-/
def functionOracleExternalAmplitudeSourceContract :
    FunctionOracleExternalAmplitudeSourceContract where
  sourceAnchor :=
    "GHL2025 Theorem 'Amplitude-oracle for piece-wise polynomial function' and Eq. 'coordinate oracle', arXiv:2506.20478; cited source arXiv:2411.01131"
  theoremAnchor :=
    "GHL2025 Theorem 'Amplitude-oracle for piece-wise polynomial function'"
  coordinateOracleAnchor := "GHL2025 Eq. 'coordinate oracle'"
  citedSourceAnchor :=
    "Guseynov-Liu 2024, arXiv:2411.01131, Theorem 5"
  cleanBranchFormula := "f(x_i) / N_f"
  normalizerNf := Coeff.symbol "N_f"
  resourceClaim := {
    description := "transcribe the O_f gate count O(sum_g Q_g n log n) and n - 1 pure ancillas from the cited theorem"
    source := "GHL2025 Theorem amplitude-oracle for piece-wise polynomial function, arXiv:2506.20478; Guseynov-Liu 2024, arXiv:2411.01131"
    proved := false
  }
  externalTheoremFormalized := {
    description := "formalize or contract the cited GL2024 Theorem 5 amplitude-oracle result before using it as a Lean proof"
    source := "Guseynov-Liu 2024, arXiv:2411.01131, Theorem 5"
    proved := false
  }
  nonzeroNormalizer := {
    description := "prove N_f is nonzero before interpreting f(x_i) / N_f"
    source := "Guseynov-Huang-Liu 2025, coordinate-oracle equation, arXiv:2506.20478"
    proved := false
  }
  divisionSemantics := {
    description := "interpret the formal function value times N_f_inv as f(x_i) / N_f"
    source := "Guseynov-Huang-Liu 2025, coordinate-oracle equation, arXiv:2506.20478"
    proved := false
  }
  theoremAmplitudeCorrect := {
    description := "FunctionOracleContract amplitudeCorrect for O_f remains to be proved from the clean branch and orthogonal completion"
    source := "Guseynov-Huang-Liu 2025, amplitude-oracle theorem and coordinate-oracle equation, arXiv:2506.20478"
    proved := false
  }
  closesNormalizerBound := false
  closesOrthogonalCompletion := false
  closesUnitaryCompletion := false
  closesFunctionOracleContract := false

theorem functionOracleExternalAmplitudeSourceContract_sourceAnchor :
    functionOracleExternalAmplitudeSourceContract.sourceAnchor =
      "GHL2025 Theorem 'Amplitude-oracle for piece-wise polynomial function' and Eq. 'coordinate oracle', arXiv:2506.20478; cited source arXiv:2411.01131" := rfl

theorem functionOracleExternalAmplitudeSourceContract_flags_false :
    functionOracleExternalAmplitudeSourceContract.resourceClaim.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.externalTheoremFormalized.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.nonzeroNormalizer.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.divisionSemantics.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.theoremAmplitudeCorrect.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.closesNormalizerBound = false ∧
      functionOracleExternalAmplitudeSourceContract.closesOrthogonalCompletion = false ∧
      functionOracleExternalAmplitudeSourceContract.closesUnitaryCompletion = false ∧
      functionOracleExternalAmplitudeSourceContract.closesFunctionOracleContract = false := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/--
Refined proof route for the `of_nf_amplitude_route` block.

The route ties the paper's coordinate-oracle equation to the current Lean
source-contract data: the symbolic function value, the `N_f` normalizer symbol,
the clean-branch amplitude in `functionOraclePaperImage`, and the theorem-level
function-oracle obligation.  It does not prove that `N_f` is nonzero, that
`N_f_inv` is an inverse, that the normalizer bound holds, or that the
orthogonal component gives a unitary completion.
-/
structure FunctionOracleAmplitudeProofRoute where
  sourceAnchor : String
  systemValue : Nat
  sourceFunctionValue : Coeff
  normalizerNf : Coeff
  normalizedAmplitude : Coeff
  normalizedAmplitudeFormula : String
  cleanBranchAmplitude : Coeff
  cleanBranchBasisIndex : Nat
  cleanWorkspaceBranch : Bool
  theoremNormalizer : Coeff
  normalizedAmplitudeCorrect : ObligationRecord
  nonzeroNormalizer : ObligationRecord
  divisionSemantics : ObligationRecord
  normalizerBound : ObligationRecord
  orthogonalComponentCorrect : ObligationRecord
  unitaryCompletion : ObligationRecord
  theoremAmplitudeCorrect : ObligationRecord
deriving Repr, DecidableEq

/--
Default O_f amplitude-route contract for one compound basis column.

The route reuses `functionOraclePaperImage`; it only packages the dependencies
needed before any future proof of the clean-branch amplitude or theorem-level
`FunctionOracleContract.amplitudeCorrect` field.
-/
def functionOracleAmplitudeProofRoute
    (p : OneTermRobinParameters) (j : Nat) :
    FunctionOracleAmplitudeProofRoute :=
  let image := functionOraclePaperImage p j
  let source := functionOracleExternalAmplitudeSourceContract
  {
    sourceAnchor := source.sourceAnchor
    systemValue := image.cleanBranchSystemValue
    sourceFunctionValue := robinFunctionValue p.n image.cleanBranchSystemValue
    normalizerNf := source.normalizerNf
    normalizedAmplitude := functionOracleNormalizedValue p image.cleanBranchSystemValue
    normalizedAmplitudeFormula := source.cleanBranchFormula
    cleanBranchAmplitude := image.cleanBranchAmplitude
    cleanBranchBasisIndex := image.cleanBranchBasisIndex
    cleanWorkspaceBranch := image.cleanWorkspaceBranch
    theoremNormalizer := source.normalizerNf
    normalizedAmplitudeCorrect := image.normalizedAmplitudeCorrect
    nonzeroNormalizer := source.nonzeroNormalizer
    divisionSemantics := source.divisionSemantics
    normalizerBound := image.normalizerBound
    orthogonalComponentCorrect := image.orthogonalComponentCorrect
    unitaryCompletion := image.unitaryCompletion
    theoremAmplitudeCorrect := source.theoremAmplitudeCorrect
  }

theorem functionOracleAmplitudeProofRoute_sourceAnchor
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).sourceAnchor =
      "GHL2025 Theorem 'Amplitude-oracle for piece-wise polynomial function' and Eq. 'coordinate oracle', arXiv:2506.20478; cited source arXiv:2411.01131" := rfl

theorem functionOracleAmplitudeProofRoute_sourceFunctionValue
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).sourceFunctionValue =
      robinFunctionValue p.n (functionOraclePaperRegisters p j).systemValue := rfl

theorem functionOracleAmplitudeProofRoute_normalizerNf
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).normalizerNf =
      Coeff.symbol "N_f" := rfl

theorem functionOracleAmplitudeProofRoute_normalizedAmplitude
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).normalizedAmplitude =
      functionOracleNormalizedValue p (functionOraclePaperRegisters p j).systemValue := rfl

theorem functionOracleAmplitudeProofRoute_paperImage
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).cleanBranchAmplitude =
      (functionOraclePaperImage p j).cleanBranchAmplitude ∧
    (functionOracleAmplitudeProofRoute p j).cleanBranchBasisIndex =
      (functionOraclePaperImage p j).cleanBranchBasisIndex ∧
    (functionOracleAmplitudeProofRoute p j).cleanWorkspaceBranch =
      (functionOraclePaperImage p j).cleanWorkspaceBranch := by
  exact ⟨rfl, rfl, rfl⟩

theorem functionOracleAmplitudeProofRoute_obligations_reuse_paperImage
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).normalizedAmplitudeCorrect =
      (functionOraclePaperImage p j).normalizedAmplitudeCorrect ∧
    (functionOracleAmplitudeProofRoute p j).normalizerBound =
      (functionOraclePaperImage p j).normalizerBound ∧
    (functionOracleAmplitudeProofRoute p j).orthogonalComponentCorrect =
      (functionOraclePaperImage p j).orthogonalComponentCorrect ∧
    (functionOracleAmplitudeProofRoute p j).unitaryCompletion =
      (functionOraclePaperImage p j).unitaryCompletion := by
  exact ⟨rfl, rfl, rfl, rfl⟩

theorem functionOracleAmplitudeProofRoute_externalSourceContract
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).sourceAnchor =
      functionOracleExternalAmplitudeSourceContract.sourceAnchor ∧
    (functionOracleAmplitudeProofRoute p j).normalizerNf =
      functionOracleExternalAmplitudeSourceContract.normalizerNf ∧
    (functionOracleAmplitudeProofRoute p j).normalizedAmplitudeFormula =
      functionOracleExternalAmplitudeSourceContract.cleanBranchFormula ∧
    (functionOracleAmplitudeProofRoute p j).nonzeroNormalizer =
      functionOracleExternalAmplitudeSourceContract.nonzeroNormalizer ∧
    (functionOracleAmplitudeProofRoute p j).divisionSemantics =
      functionOracleExternalAmplitudeSourceContract.divisionSemantics ∧
    (functionOracleAmplitudeProofRoute p j).theoremAmplitudeCorrect =
      functionOracleExternalAmplitudeSourceContract.theoremAmplitudeCorrect := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem functionOracleAmplitudeProofRoute_flags_false
    (p : OneTermRobinParameters) (j : Nat) :
    (functionOracleAmplitudeProofRoute p j).normalizedAmplitudeCorrect.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).nonzeroNormalizer.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).divisionSemantics.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).normalizerBound.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).orthogonalComponentCorrect.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).unitaryCompletion.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).theoremAmplitudeCorrect.proved = false := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/--
Combined Phase-1 guard for the `O_f` external-source route.

The bridge to the cited amplitude-oracle theorem and the false analytic flags
are packaged together so later proof packets cannot use the source transcript
as a proof of `O_f` amplitude correctness or unitarity.
-/
theorem functionOracleAmplitudeProofRoute_externalSourceAndFlags
    (p : OneTermRobinParameters) (j : Nat) :
    ((functionOracleAmplitudeProofRoute p j).sourceAnchor =
        functionOracleExternalAmplitudeSourceContract.sourceAnchor ∧
      (functionOracleAmplitudeProofRoute p j).normalizerNf =
        functionOracleExternalAmplitudeSourceContract.normalizerNf ∧
      (functionOracleAmplitudeProofRoute p j).normalizedAmplitudeFormula =
        functionOracleExternalAmplitudeSourceContract.cleanBranchFormula ∧
      (functionOracleAmplitudeProofRoute p j).nonzeroNormalizer =
        functionOracleExternalAmplitudeSourceContract.nonzeroNormalizer ∧
      (functionOracleAmplitudeProofRoute p j).divisionSemantics =
        functionOracleExternalAmplitudeSourceContract.divisionSemantics ∧
      (functionOracleAmplitudeProofRoute p j).theoremAmplitudeCorrect =
        functionOracleExternalAmplitudeSourceContract.theoremAmplitudeCorrect) ∧
    (functionOracleExternalAmplitudeSourceContract.resourceClaim.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.externalTheoremFormalized.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.nonzeroNormalizer.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.divisionSemantics.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.theoremAmplitudeCorrect.proved = false ∧
      functionOracleExternalAmplitudeSourceContract.closesNormalizerBound = false ∧
      functionOracleExternalAmplitudeSourceContract.closesOrthogonalCompletion = false ∧
      functionOracleExternalAmplitudeSourceContract.closesUnitaryCompletion = false ∧
      functionOracleExternalAmplitudeSourceContract.closesFunctionOracleContract = false) ∧
    (functionOracleAmplitudeProofRoute p j).normalizedAmplitudeCorrect.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).nonzeroNormalizer.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).divisionSemantics.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).normalizerBound.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).orthogonalComponentCorrect.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).unitaryCompletion.proved = false ∧
    (functionOracleAmplitudeProofRoute p j).theoremAmplitudeCorrect.proved = false := by
  exact ⟨
    functionOracleAmplitudeProofRoute_externalSourceContract p j,
    functionOracleExternalAmplitudeSourceContract_flags_false,
    functionOracleAmplitudeProofRoute_flags_false p j⟩

/--
Symbolic matrix entry for the unresolved orthogonal component of `O_f`.

The paper only fixes the clean `m_f` branch amplitude
`f(x_i) / N_f`; the remaining orthogonal completion is a unitarity obligation.
This symbol records one placeholder entry for that unresolved completion without
proving orthogonality, normalizer bounds, or unitarity.
-/
def functionOracleOrthogonalEntry
    (p : OneTermRobinParameters) (systemValue row col : Nat) : Coeff :=
  Coeff.symbol s!"orth_f_entry_{p.n}_{systemValue}_{row}_{col}"

/--
Faithful Phase 1 matrix skeleton for the paper-level function oracle `O_f`.

For each clean-workspace input column, the clean `m_f` branch entry is the
normalized amplitude recorded by `functionOraclePaperImage`, namely
`f(x_i) / N_f` represented as `functionOracleNormalizedValue`.  Other
clean-workspace output rows are zero, matching the paper statement that the
unresolved component is orthogonal to the clean workspace branch.
Non-clean-workspace rows carry symbolic completion entries.  For non-clean
input columns, the paper does not fix a branch equation, so this skeleton leaves
all entries symbolic.

The symbolic completion does not prove amplitude correctness, the `N_f` bound,
orthogonality, or unitarity; those obligations remain false in
`functionOraclePaperImage` and the gate record.
-/
def functionOraclePaperMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let image := functionOraclePaperImage p j.val
    if image.cleanWorkspaceBranch then
      if i.val = image.cleanBranchBasisIndex then
        image.cleanBranchAmplitude
      else if (functionOraclePaperRegisters p i.val).mfWorkspaceValue = 0 then
        Coeff.rat 0
      else
        functionOracleOrthogonalEntry p image.cleanBranchSystemValue i.val j.val
    else
      functionOracleOrthogonalEntry p image.cleanBranchSystemValue i.val j.val

/-- The `O_f` paper matrix exposes the clean branch amplitude for clean input columns. -/
theorem functionOraclePaperMatrix_cleanBranch_entry
    (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hClean : (functionOraclePaperImage p j.val).cleanWorkspaceBranch = true)
    (h : i.val = (functionOraclePaperImage p j.val).cleanBranchBasisIndex) :
    functionOraclePaperMatrix p i j =
      (functionOraclePaperImage p j.val).cleanBranchAmplitude := by
  simp [functionOraclePaperMatrix, hClean, h]

/-- Other clean-workspace rows have zero `O_f` orthogonal-completion entry. -/
theorem functionOraclePaperMatrix_cleanWorkspace_offBranch_zero
    (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hInputClean : (functionOraclePaperImage p j.val).cleanWorkspaceBranch = true)
    (hBranch : i.val ≠ (functionOraclePaperImage p j.val).cleanBranchBasisIndex)
    (hClean : (functionOraclePaperRegisters p i.val).mfWorkspaceValue = 0) :
    functionOraclePaperMatrix p i j = Coeff.rat 0 := by
  simp [functionOraclePaperMatrix, hInputClean, hBranch, hClean]

/-- Non-clean input columns are left in the symbolic `O_f` completion branch. -/
theorem functionOraclePaperMatrix_nonCleanInput_entry
    (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hInputNonClean : (functionOraclePaperImage p j.val).cleanWorkspaceBranch = false) :
    functionOraclePaperMatrix p i j =
      functionOracleOrthogonalEntry p
        (functionOraclePaperImage p j.val).cleanBranchSystemValue i.val j.val := by
  simp [functionOraclePaperMatrix, hInputNonClean]

/--
Helper-only O_f diagonal matrix: records function values f(x_j) on the diagonal.

For each compound basis state |j⟩, extracts the system register value i
and sets the diagonal entry to `robinFunctionValue n i` = Coeff.symbol "f_x_i".
All off-diagonal entries are zero.  The entry depends only on the system
register (grid point index), not on the sparse index.

The paper's O_f (Theorem amplitude-oracle for piece-wise polynomial function,
main.tex:870-910) encodes f(x_j)/N_f via amplitude oracle.  The 1/N_f
normalization is absorbed into the block-encoding normalizer
α = N_D · N_f · κ.  This diagonal matrix is not the paper image; the
paper-level clean branch and orthogonal-component obligations are recorded by
`functionOraclePaperImage`, and the active gate keeps `unitary.proved := false`.

main.tex:870-910 --/
def functionOracleMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    if i.val = j.val then
      let n := p.n
      let sysMask := (1 <<< n) - 1
      let sysVal := (j.val >>> 1) &&& sysMask
      robinFunctionValue n sysVal
    else Coeff.rat 0

/--
Gate matrix for `O_f` using the faithful paper-image matrix skeleton.

The active matrix now exposes the clean `m_f` branch amplitude from
`functionOraclePaperImage`.  The legacy diagonal helper `functionOracleMatrix`
remains available only as a function-value data check.  Unitarity, amplitude
correctness, the `N_f` bound, and the orthogonal completion are still unproved.
Guseynov-Huang-Liu 2025, Theorem amplitude-oracle for piece-wise polynomial
function and Fig. 1-term Robin, arXiv:2506.20478. -/
def oneTermRobinGate_O_f (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "O_f"
  matrix := functionOraclePaperMatrix p
  unitary := {
    description := "O_f paper-image matrix skeleton: clean branch wired, orthogonal completion and unitarity not yet proved"
    source := "Guseynov-Huang-Liu 2025, Theorem amplitude-oracle for piece-wise polynomial function and Fig. 1-term Robin, arXiv:2506.20478"
    proved := false
  }

/--
Honest SWAP matrix: permutation matrix swapping the system register
(n qubits at bits [1, 1+n)) with the O_D^BS register (n qubits at bits [1+n, 1+2n)).

For each basis state |j⟩:
  - Extract block1 = bits [1, 1+n) of j  (system register value)
  - Extract block2 = bits [1+n, 1+2n) of j (O_D^BS register value)
  - diff = block1 XOR block2
  - Swapped index = j XOR (diff <<< 1) XOR (diff <<< (1+n))

When block1 = block2 the SWAP is the identity.  All bits outside the two
n-qubit blocks (ancilla bit 0, indicator bit 1+2n, mf MSBs) are preserved.

  The SWAP image-level proof is now promoted: `swapOracleImage` is proved
  self-inverse, `swapOracleMatrix` is proved a finite permutation matrix, and
  `oneTermRobinGate_SWAP.unitary.proved = true`.
  figure:1_term_ROBIN, main.tex:1140 --/
def swapOracleMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let n := p.n
    let blockMask := (1 <<< n) - 1
    let block1 := (j.val >>> 1) &&& blockMask
    let block2 := (j.val >>> (1 + n)) &&& blockMask
    let diff := block1 ^^^ block2
    let swapped := j.val ^^^ (diff <<< 1) ^^^ (diff <<< (1 + n))
    if i.val = swapped then Coeff.rat 1 else Coeff.rat 0

/--
Image function for the SWAP oracle: swaps two n-qubit register blocks.
For each basis state j, swaps block1 (bits [1,1+n)) with block2 (bits [1+n,1+2n))
by XORing with the block difference shifted to each block position.
main.tex:1140 --/
def swapOracleImage (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let n := p.n
  let blockMask := (1 <<< n) - 1
  let block1 := (j >>> 1) &&& blockMask
  let block2 := (j >>> (1 + n)) &&& blockMask
  let diff := block1 ^^^ block2
  j ^^^ (diff <<< 1) ^^^ (diff <<< (1 + n))

/--
The n-bit XOR difference between the two register blocks exchanged by SWAP.

This is the reusable proof-DAG interface for the SWAP image route: preservation
of this value after one SWAP is the local ingredient for self-inverse and later
finite-domain permutation proofs.
-/
def swapOracleDiff (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let n := p.n
  let blockMask := (1 <<< n) - 1
  let block1 := (j >>> 1) &&& blockMask
  let block2 := (j >>> (1 + n)) &&& blockMask
  block1 ^^^ block2

/-- The SWAP image is the source index XORed by the same difference in both blocks. -/
theorem swapOracleImage_eq_xor_diff (p : OneTermRobinParameters) (j : Nat) :
    swapOracleImage p j =
      j ^^^ (swapOracleDiff p j <<< 1) ^^^
        (swapOracleDiff p j <<< (1 + p.n)) := by
  rfl

/-- swapOracleMatrix entry equals image function check. -/
theorem swapOracleMatrix_eq_image (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    swapOracleMatrix p i j =
      if i.val = swapOracleImage p j.val then Coeff.rat 1 else Coeff.rat 0 := by
  simp [swapOracleMatrix, swapOracleImage] <;> rfl

/--
Gate matrix for SWAP using the honest permutation matrix.
Swaps system register (bits [1,n+1)) with O_D^BS register (bits [n+1,2n+1)).
Unitarity is backed by the proof-DAG permutation bridge below:
`swapOracleMatrix_is_permutation`.
main.tex:1140 --/
def oneTermRobinGate_SWAP (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.swap 0 0
  matrix := swapOracleMatrix p
  unitary := {
    description := "SWAP permutation matrix: unitarity backed by swapOracleMatrix_is_permutation"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin SWAP operation, arXiv:2506.20478"
    proved := true
  }

/--
Transpose-style matrix for O_D^BS, sharing the forward sparse-access image map.
For each i: compute image(i) using the forward mapping, then check if j = image(i).
This is the matrix transpose of bandedSparseAccessMatrix.  The inverse/unitarity
proof is blocked until the forward boundary column-map contract is reconciled.
main.tex:1148 --/
def bandedSparseAccessDaggerMatrix (p : OneTermRobinParameters) :
    Matrix (qubitDim (oneTermRobinTotalQubits p)) (qubitDim (oneTermRobinTotalQubits p)) Coeff :=
  fun i j =>
    let n := p.n
    let kappa := p.kappa
    let κbits := clog2 kappa
    let odPure := n - κbits
    let sysMask := (1 <<< n) - 1
    let sysVal := (i.val >>> 1) &&& sysMask
    let sparseStart := 1 + n + odPure
    let sparseMask := (1 <<< κbits) - 1
    let sparseVal := (i.val >>> sparseStart) &&& sparseMask
    let col := robinSparseColumnMap n sparseVal sysVal
    let image := i.val - (i.val &&& (sysMask <<< 1)) + (col <<< 1)
    if j.val = image then Coeff.rat 1 else Coeff.rat 0

/--
Gate matrix for `(O_D^BS)^†` using the transpose-style paper-image matrix.

This is paired with `bandedSparseAccessPaperMatrix`; it does not prove that the
transpose is a true inverse on the relevant post-SWAP states.
figure:1_term_ROBIN and Lemma 1, arXiv:2506.20478. -/
def oneTermRobinGate_O_D_BS_dagger (p : OneTermRobinParameters) : GateMatrix Coeff (oneTermRobinTotalQubits p) where
  gate := Gate.oracleCall "(O_D^BS)^†"
  matrix := bandedSparseAccessPaperDaggerMatrix p
  unitary := {
    description := "(O_D^BS)^† paper-image transpose matrix: cleanup and unitarity not yet proved"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- Active `(O_D^BS)^†` gate entry paired with the finite forward image. -/
theorem oneTermRobinGate_O_D_BS_dagger_imageFin_eq_one
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    (oneTermRobinGate_O_D_BS_dagger p).matrix j
        (bandedSparseAccessPaperImageFin p j haddr) =
      Coeff.rat 1 := by
  simpa [oneTermRobinGate_O_D_BS_dagger]
    using bandedSparseAccessPaperDaggerMatrix_imageFin_eq_one p j haddr

/--
Post-SWAP dagger entry from an explicitly supplied paper-image preimage.

The hypothesis `hpre` is the whole inverse-on-range input for this lemma:
it does not prove that such a `pre` exists, that it is unique, or that the
dagger cleans the padded sparse-index register.  The post-SWAP relation is
recorded by `hpost` for the cleanup proof-DAG interface, but the matrix entry
itself is just the active transpose-style paper-image entry.
-/
theorem oneTermRobinGate_O_D_BS_dagger_postSwap_entry_of_preimage
    (p : OneTermRobinParameters)
    (source post pre : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hpost : post.val =
      swapOracleImage p
        (bandedSparseAccessPaperImage p source.val))
    (hpre : post.val = bandedSparseAccessPaperImage p pre.val) :
    (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1 := by
  have _postSwapWitness :
      post.val = swapOracleImage p (bandedSparseAccessPaperImage p source.val) := hpost
  simp [oneTermRobinGate_O_D_BS_dagger, bandedSparseAccessPaperDaggerMatrix, hpre]

/--
Proof-carrying interface for a supplied post-SWAP cleanup preimage.

The fields intentionally include the hypotheses that are not yet derived:
`postSwap`, `preimage`, `preCleanInput`, and `preAddressBound`.  The record only
packages consequences of those inputs: the active dagger entry and executable
register-cleanup checks for the chosen preimage.  Existence, uniqueness, and
the paper-level `daggerCleanup` obligation remain open.
-/
structure BandedSparseAccessPostSwapCleanup
    (p : OneTermRobinParameters)
    (source post pre : Fin (qubitDim (oneTermRobinTotalQubits p))) where
  postSwap :
    post.val = swapOracleImage p (bandedSparseAccessPaperImage p source.val)
  preimage : post.val = bandedSparseAccessPaperImage p pre.val
  preCleanInput : bandedSparseAccessPaperCleanInput p pre.val = true
  preAddressBound : bandedSparseAccessPaperAddress p pre.val < (1 <<< p.n)
  daggerEntry : (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1
  preRowPreserved :
    (bandedSparseAccessPaperColumnContract p pre.val).rowPreserved = true
  preAddressWritten :
    (bandedSparseAccessPaperColumnContract p pre.val).addressWritten = true
  preAddressInRange :
    (bandedSparseAccessPaperColumnContract p pre.val).addressInRange = true
  preImageNoSpill :
    (bandedSparseAccessPaperColumnContract p pre.val).imageNoSpill = true
  postRow_eq_preRow :
    (bandedSparseAccessPaperRegisters p post.val).rowValue =
      (bandedSparseAccessPaperRegisters p pre.val).rowValue
  postOd_eq_preAddress :
    (bandedSparseAccessPaperRegisters p post.val).odRegisterValue =
      bandedSparseAccessPaperAddress p pre.val

/--
Build the post-SWAP cleanup witness from an explicitly supplied preimage.

This is the fixed inverse-on-range interface for the next cleanup proof: it
does not construct the preimage and does not promote any semantic proof flag.
-/
def bandedSparseAccessPostSwapCleanup_of_preimage
    (p : OneTermRobinParameters)
    (source post pre : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hpost : post.val =
      swapOracleImage p
        (bandedSparseAccessPaperImage p source.val))
    (hpre : post.val = bandedSparseAccessPaperImage p pre.val)
    (hclean : bandedSparseAccessPaperCleanInput p pre.val = true)
    (haddr : bandedSparseAccessPaperAddress p pre.val < (1 <<< p.n)) :
    BandedSparseAccessPostSwapCleanup p source post pre := by
  let hsafety :=
    bandedSparseAccessPaperColumnContract_registerSafety_of_address_lt
      p pre.val haddr
  exact {
    postSwap := hpost
    preimage := hpre
    preCleanInput := hclean
    preAddressBound := haddr
    daggerEntry :=
      oneTermRobinGate_O_D_BS_dagger_postSwap_entry_of_preimage
        p source post pre hpost hpre
    preRowPreserved := hsafety.1
    preAddressWritten := hsafety.2.1
    preAddressInRange := hsafety.2.2.1
    preImageNoSpill := hsafety.2.2.2
    postRow_eq_preRow := by
      rw [hpre]
      exact bandedSparseAccessPaperImage_rowValue_eq p pre.val
    postOd_eq_preAddress := by
      rw [hpre]
      exact bandedSparseAccessPaperImage_odRegisterValue_eq p pre.val haddr
  }

/--
Reusable image witness for the active Lemma 1 `O_D^BS` gate pair.

This packages the forward entry, transpose-style dagger entry, row roundtrip,
written-address roundtrip, and no-spill Boolean under the explicit n-bit
address hypothesis.  It is not an injectivity, inverse uniqueness, cleanup, or
unitarity proof.
-/
theorem oneTermRobinGate_O_D_BS_imageFin_entrySafety
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n)) :
    (oneTermRobinGate_O_D_BS p).matrix
        (bandedSparseAccessPaperImageFin p j haddr) j = Coeff.rat 1 ∧
      (oneTermRobinGate_O_D_BS_dagger p).matrix j
        (bandedSparseAccessPaperImageFin p j haddr) = Coeff.rat 1 ∧
      (bandedSparseAccessPaperRegisters p
        (bandedSparseAccessPaperImage p j.val)).rowValue =
          (bandedSparseAccessPaperRegisters p j.val).rowValue ∧
      (bandedSparseAccessPaperRegisters p
        (bandedSparseAccessPaperImage p j.val)).odRegisterValue =
          bandedSparseAccessPaperAddress p j.val ∧
      bandedSparseAccessPaperImageNoSpill p j.val = true := by
  constructor
  · exact oneTermRobinGate_O_D_BS_imageFin_eq_one p j haddr
  constructor
  · exact oneTermRobinGate_O_D_BS_dagger_imageFin_eq_one p j haddr
  constructor
  · exact bandedSparseAccessPaperImage_rowValue_eq p j.val
  constructor
  · exact bandedSparseAccessPaperImage_odRegisterValue_eq p j.val haddr
  · exact bandedSparseAccessPaperImageNoSpill_eq_true_of_address_lt p j.val haddr

/--
Global-source specialization of the active Lemma 1 `O_D^BS` entry witness.

For a finite column in the faithful source domain, the global-slot source
predicate supplies the clean padded input and sparse-slot bound, while the
`2 <= n` parameter-family hypothesis supplies the n-bit address bound.  The
result packages the finite image index and paired forward/dagger entries, but
does not prove injectivity, cleanup, or unitarity.
-/
theorem oneTermRobinGate_O_D_BS_globalSlotSource_entrySafety
    (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 2 ≤ p.n)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p j.val = true) :
    bandedSparseAccessPaperCleanInput p j.val = true ∧
      (bandedSparseAccessPaperRegisters p j.val).sparseIndexValue < p.kappa ∧
      ∃ image : Fin (qubitDim (oneTermRobinTotalQubits p)),
        image.val = bandedSparseAccessPaperImage p j.val ∧
          (oneTermRobinGate_O_D_BS p).matrix image j = Coeff.rat 1 ∧
          (oneTermRobinGate_O_D_BS_dagger p).matrix j image = Coeff.rat 1 ∧
          (bandedSparseAccessPaperRegisters p
            (bandedSparseAccessPaperImage p j.val)).rowValue =
              (bandedSparseAccessPaperRegisters p j.val).rowValue ∧
          (bandedSparseAccessPaperRegisters p
            (bandedSparseAccessPaperImage p j.val)).odRegisterValue =
              bandedSparseAccessPaperAddress p j.val ∧
          bandedSparseAccessPaperImageNoSpill p j.val = true ∧
          (oneTermRobinGate_O_D_BS p).unitary.proved = false ∧
          (oneTermRobinGate_O_D_BS_dagger p).unitary.proved = false := by
  have hclean :=
    bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
      p j.val hsource
  have hsparse :=
    bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
      p j.val hsource
  have haddrGrid :=
    bandedSparseAccessPaperAddress_lt_gridSize_of_two_le p j.val hn
  have haddr : bandedSparseAccessPaperAddress p j.val < (1 <<< p.n) := by
    simpa [gridSize, Nat.one_shiftLeft] using haddrGrid
  let image := bandedSparseAccessPaperImageFin p j haddr
  have hsafety := oneTermRobinGate_O_D_BS_imageFin_entrySafety p j haddr
  refine ⟨hclean, hsparse, image, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact bandedSparseAccessPaperImageFin_val p j haddr
  · exact hsafety.1
  · exact hsafety.2.1
  · exact hsafety.2.2.1
  · exact hsafety.2.2.2.1
  · exact hsafety.2.2.2.2
  · rfl
  · rfl

/--
List of all 7 gate matrix placeholders for the one-term Robin circuit,
in the same order as `oneTermRobinCircuit`.
figure:1_term_ROBIN --/
def oneTermRobinGateMatrixPlaceholders (p : OneTermRobinParameters) :
    List (GateMatrix Coeff (oneTermRobinTotalQubits p)) :=
  [ oneTermRobinGate_U_indic p
  , oneTermRobinGate_O_DT_S p
  , oneTermRobinGate_Ry_boundary p
  , oneTermRobinGate_O_D_BS p
  , oneTermRobinGate_O_f p
  , oneTermRobinGate_SWAP p
  , oneTermRobinGate_O_D_BS_dagger p
  ]

/--
The placeholder gate matrices match the circuit gate labels.
This is trivially true because the placeholders were constructed
with matching gate constructors.
figure:1_term_ROBIN --/
theorem oneTermRobinPlaceholdersMatch (p : OneTermRobinParameters) :
    gateMatricesMatchCircuit oneTermRobinCircuit (oneTermRobinGateMatrixPlaceholders p) = true := by
  simp [oneTermRobinCircuit, oneTermRobinGateMatrixPlaceholders,
    oneTermRobinGate_U_indic, oneTermRobinGate_O_DT_S,
    oneTermRobinGate_Ry_boundary, oneTermRobinGate_O_D_BS,
    oneTermRobinGate_O_f, oneTermRobinGate_SWAP,
    oneTermRobinGate_O_D_BS_dagger,
    gateMatricesMatchCircuit]

/--
The active matrix placeholder list uses the same gate order as Fig. 1-term
Robin and `oneTermRobinCircuit`.

This is a structural guard only: it prevents a later proof packet from keeping
similar-looking proof flags while changing the circuit order.
-/
theorem oneTermRobinGateMatrixPlaceholders_gateList
    (p : OneTermRobinParameters) :
    (oneTermRobinGateMatrixPlaceholders p).map
        (fun gateMatrix => gateMatrix.gate) =
      oneTermRobinCircuit := by
  simp [oneTermRobinCircuit, oneTermRobinGateMatrixPlaceholders,
    oneTermRobinGate_U_indic, oneTermRobinGate_O_DT_S,
    oneTermRobinGate_Ry_boundary, oneTermRobinGate_O_D_BS,
    oneTermRobinGate_O_f, oneTermRobinGate_SWAP,
    oneTermRobinGate_O_D_BS_dagger]

/--
The active seven-gate matrix list keeps only the locally certified indicator
and SWAP gates marked as proved.

This is a Phase 1 guard for Fig. 1-term Robin.  It records the current
gate-level proof flags without promoting the paper-oracle obligations for
`O_DT^S`, `Ry_boundary`, `O_D^BS`, `O_f`, or `(O_D^BS)^dagger`.
-/
theorem oneTermRobinGateMatrixPlaceholders_unitaryFlags
    (p : OneTermRobinParameters) :
    (oneTermRobinGateMatrixPlaceholders p).map
        (fun gateMatrix => gateMatrix.unitary.proved) =
      [true, false, false, false, false, true, false] := by
  simp [oneTermRobinGateMatrixPlaceholders,
    oneTermRobinGate_U_indic, oneTermRobinGate_O_DT_S,
    oneTermRobinGate_Ry_boundary, oneTermRobinGate_O_D_BS,
    oneTermRobinGate_O_f, oneTermRobinGate_SWAP,
    oneTermRobinGate_O_D_BS_dagger]

/--
Indicator oracle image function: for each basis state j, computes the image
by XORing the indicator bit at position indPos when the system register value
is in the bulk window [K1, K2]. This is a self-inverse permutation.
main.tex:1088-1099 --/
def indicatorOracleImage (p : OneTermRobinParameters) (j : Nat) : Nat :=
  let n := p.n
  let indPos := robinIndicatorBitPosition p
  let systemVal := (j >>> 1) &&& ((1 <<< n) - 1)
  let K1 := 2
  let K2 := gridSize n - 3
  let isBulk := if K1 ≤ systemVal ∧ systemVal ≤ K2 then (1 : Nat) else 0
  j ^^^ (isBulk <<< indPos)

/--
The indicator oracle matrix entry is 1 exactly when i = indicatorOracleImage j.
main.tex:1088-1099 --/
theorem indicatorOracleMatrix_eq_image (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    indicatorOracleMatrix p i j =
      if i.val = indicatorOracleImage p j.val then Coeff.rat 1 else Coeff.rat 0 := by
  simp [indicatorOracleMatrix, indicatorOracleImage] <;> rfl

/--
Self-inverse property for n=1: applying indicatorOracleImage twice returns the
original value for all j in Fin domain (128 elements).
Checked by native_decide over the finite Fin type.
main.tex:1088-1099 --/
theorem indicatorOracleImage_self_inverse_n1 :
    ∀ j : Fin (qubitDim (oneTermRobinTotalQubits
      { n := 1, kappa := 1, functionPieces := 1, polynomialDegreeCost := 1 })),
      indicatorOracleImage
        { n := 1, kappa := 1, functionPieces := 1, polynomialDegreeCost := 1 }
        (indicatorOracleImage
          { n := 1, kappa := 1, functionPieces := 1, polynomialDegreeCost := 1 } j) = j := by
  native_decide

/--
Self-inverse property for n=3: applying indicatorOracleImage twice returns the
original value for all j in Fin domain (8192 elements).
Checked by native_decide over the finite Fin type.
main.tex:1088-1099 --/
theorem indicatorOracleImage_self_inverse_n3 :
    ∀ j : Fin (qubitDim (oneTermRobinTotalQubits
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 })),
      indicatorOracleImage
        { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
        (indicatorOracleImage
          { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 } j) = j := by
  native_decide

/--
Injectivity for n=1: derived from self-inverse property.
main.tex:1088-1099 --/
theorem indicatorOracleImage_injective_n1 {j₁ j₂ : Fin (qubitDim (oneTermRobinTotalQubits
      { n := 1, kappa := 1, functionPieces := 1, polynomialDegreeCost := 1 }))}
    (h : indicatorOracleImage
        { n := 1, kappa := 1, functionPieces := 1, polynomialDegreeCost := 1 } j₁ =
      indicatorOracleImage
        { n := 1, kappa := 1, functionPieces := 1, polynomialDegreeCost := 1 } j₂) :
    j₁ = j₂ := by
  have h1 := indicatorOracleImage_self_inverse_n1 j₁
  have h2 := indicatorOracleImage_self_inverse_n1 j₂
  apply Fin.ext
  show (j₁ : Nat) = j₂
  rw [← h1, ← h2, h]

/--
Injectivity for n=3: derived from self-inverse property.
main.tex:1088-1099 --/
theorem indicatorOracleImage_injective_n3 {j₁ j₂ : Fin (qubitDim (oneTermRobinTotalQubits
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }))}
    (h : indicatorOracleImage
        { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 } j₁ =
      indicatorOracleImage
        { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 } j₂) :
    j₁ = j₂ := by
  have h1 := indicatorOracleImage_self_inverse_n3 j₁
  have h2 := indicatorOracleImage_self_inverse_n3 j₂
  apply Fin.ext
  show (j₁ : Nat) = j₂
  rw [← h1, ← h2, h]

/--
Cycle 12 helper: (b <<< pos) &&& ((1 <<< n) - 1) = 0 when pos >= n,
because b <<< pos has all zeros in bits [0, pos) >= [0, n).
-/
theorem shiftLeft_land_mask_eq_zero (b pos n : Nat) (h : pos ≥ n) :
    (b <<< pos) &&& ((1 <<< n) - 1) = 0 := by
  have key : ∀ i, i < n → (b <<< pos).testBit i = false := by
    intro i hi; simp [Nat.testBit_shiftLeft]; omega
  have all_false : ∀ i, (b <<< pos &&& (1 <<< n - 1)).testBit i = (0 : Nat).testBit i := by
    intro i; simp only [Nat.testBit_and]
    by_cases h1 : i < n
    · rw [key i h1]; simp
    · have : (1 <<< n - 1).testBit i = false := by
        rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]; simp [h1]
      simp [this]
  exact Nat.eq_of_testBit_eq all_false

/--
Cycle 12 helper: XOR with a value shifted left by `pos` preserves the low `n` bits
when `pos >= n`.  Uses AND-XOR distributivity and the zero mask lemma.
-/
theorem xor_shift_preserve_low (x b pos n : Nat) (h : pos ≥ n) :
    (x ^^^ (b <<< pos)) &&& ((1 <<< n) - 1) = x &&& ((1 <<< n) - 1) := by
  rw [Nat.and_xor_distrib_right]
  have := shiftLeft_land_mask_eq_zero b pos n h
  rw [this, Nat.xor_zero]

/--
Cycle 12 helper: XOR with a high-shifted value preserves low bits after right-shifting.
((x ^^^ (b <<< pos)) >>> 1) &&& ((1 <<< n) - 1) = (x >>> 1) &&& ((1 <<< n) - 1)
when pos >= 1 + n.
-/
theorem xor_shift_preserve_shift_low (x b pos n : Nat) (h : pos ≥ 1 + n) :
    ((x ^^^ (b <<< pos)) >>> 1) &&& ((1 <<< n) - 1) =
    (x >>> 1) &&& ((1 <<< n) - 1) := by
  have key : ∀ i, i < n →
      ((x ^^^ (b <<< pos)) >>> 1).testBit i = (x >>> 1).testBit i := by
    intro i hi
    simp only [Nat.testBit_shiftRight, Nat.testBit_xor]
    have : (b <<< pos).testBit (1 + i) = false := by
      simp [Nat.testBit_shiftLeft]; omega
    simp [this]
  have eq_bits : ∀ i,
      ((x ^^^ (b <<< pos)) >>> 1 &&& (1 <<< n - 1)).testBit i =
      ((x >>> 1) &&& (1 <<< n - 1)).testBit i := by
    intro i; simp only [Nat.testBit_and]
    by_cases h1 : i < n
    · simp [key i h1]
    · have : (1 <<< n - 1).testBit i = false := by
        rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]; simp [h1]
      simp [this]
  exact Nat.eq_of_testBit_eq eq_bits

/--
SWAP proof-DAG helper: the XOR difference between the two n-bit blocks is
itself an n-bit value.
main.tex:1140 --/
theorem swapOracleDiff_lt_two_pow (p : OneTermRobinParameters) (j : Nat) :
    let n := p.n
    let blockMask := (1 <<< n) - 1
    let block1 := (j >>> 1) &&& blockMask
    let block2 := (j >>> (1 + n)) &&& blockMask
    block1 ^^^ block2 < 2 ^ n := by
  dsimp
  apply Nat.xor_lt_two_pow
  · apply Nat.and_lt_two_pow
    rw [Nat.one_shiftLeft]
    exact Nat.sub_lt (Nat.pow_pos (by decide : 0 < 2) : 0 < 2 ^ p.n) (by decide)
  · apply Nat.and_lt_two_pow
    rw [Nat.one_shiftLeft]
    exact Nat.sub_lt (Nat.pow_pos (by decide : 0 < 2) : 0 < 2 ^ p.n) (by decide)

/--
SWAP proof-DAG helper: right-shifting the n-bit block difference by n removes it.
main.tex:1140 --/
theorem swapOracleDiff_shiftRight_eq_zero (p : OneTermRobinParameters) (j : Nat) :
    let n := p.n
    let blockMask := (1 <<< n) - 1
    let block1 := (j >>> 1) &&& blockMask
    let block2 := (j >>> (1 + n)) &&& blockMask
    let diff := block1 ^^^ block2
    diff >>> n = 0 := by
  have hdiff := swapOracleDiff_lt_two_pow p j
  dsimp at hdiff ⊢
  exact Nat.shiftRight_eq_zero _ _ hdiff

/--
SWAP proof-DAG helper: shifting the block difference into the high block leaves
zero in the low n-bit mask.
main.tex:1140 --/
theorem swapOracleDiff_shiftLeft_mask_eq_zero (p : OneTermRobinParameters) (j : Nat) :
    let n := p.n
    let blockMask := (1 <<< n) - 1
    let block1 := (j >>> 1) &&& blockMask
    let block2 := (j >>> (1 + n)) &&& blockMask
    let diff := block1 ^^^ block2
    (diff <<< n) &&& blockMask = 0 := by
  dsimp
  exact shiftLeft_land_mask_eq_zero
    (((j >>> 1) &&& (1 <<< p.n) - 1) ^^^ ((j >>> (1 + p.n)) &&& (1 <<< p.n) - 1))
    p.n p.n (by omega)

/-- Shifting a bounded value into a register block keeps it inside the total basis width. -/
theorem shiftLeft_lt_two_pow_of_lt
    {x width shift total : Nat}
    (hx : x < 2 ^ width) (hblock : width + shift ≤ total) :
    x <<< shift < 2 ^ total := by
  rw [Nat.shiftLeft_eq]
  have hmul : x * 2 ^ shift < 2 ^ width * 2 ^ shift :=
    Nat.mul_lt_mul_of_pos_right hx (Nat.pow_pos (by decide : 0 < 2))
  have hpow : 2 ^ width * 2 ^ shift = 2 ^ (width + shift) := by
    rw [← Nat.pow_add]
  have hle : 2 ^ (width + shift) ≤ 2 ^ total :=
    Nat.pow_le_pow_right (by decide : 0 < 2) hblock
  exact Nat.lt_of_lt_of_le (by simpa [hpow] using hmul) hle

/--
SWAP proof-DAG range block: the image of the register-block SWAP stays inside
the same full finite basis.  This is only a range lemma; the finite
permutation bridge is proved separately by `swapOracleMatrix_is_permutation`.
-/
theorem swapOracleImage_lt_qubitDim
    (p : OneTermRobinParameters) {j : Nat}
    (hj : j < qubitDim (oneTermRobinTotalQubits p)) :
    swapOracleImage p j < qubitDim (oneTermRobinTotalQubits p) := by
  simp only [qubitDim, gridSize] at hj ⊢
  unfold swapOracleImage
  let n := p.n
  let blockMask := (1 <<< n) - 1
  let block1 := (j >>> 1) &&& blockMask
  let block2 := (j >>> (1 + n)) &&& blockMask
  let diff := block1 ^^^ block2
  have hdiff : diff < 2 ^ p.n := by
    have h := swapOracleDiff_lt_two_pow p j
    simpa [n, blockMask, block1, block2, diff] using h
  have hshiftLow : diff <<< 1 < 2 ^ oneTermRobinTotalQubits p :=
    shiftLeft_lt_two_pow_of_lt hdiff (by
      have hhigh := bandedSparseAccessPaperHighWidth_le_totalQubits p
      omega)
  have hxorLow : j ^^^ (diff <<< 1) < 2 ^ oneTermRobinTotalQubits p :=
    Nat.xor_lt_two_pow hj hshiftLow
  have hshiftHigh : diff <<< (1 + n) < 2 ^ oneTermRobinTotalQubits p :=
    shiftLeft_lt_two_pow_of_lt hdiff (by
      have hhigh := bandedSparseAccessPaperHighWidth_le_totalQubits p
      omega)
  exact Nat.xor_lt_two_pow hxorLow hshiftHigh

/--
SWAP proof-DAG block: after `swapOracleImage`, the low n-bit register equals
the old high n-bit register.  This is the first register-level bit-slice lemma
needed for the eventual SWAP self-inverse/permutation proof.
main.tex:1140 --/
theorem swapOracleImage_block1_eq_block2 (p : OneTermRobinParameters) (j : Nat) :
    let n := p.n
    let blockMask := (1 <<< n) - 1
    ((swapOracleImage p j) >>> 1) &&& blockMask =
      (j >>> (1 + n)) &&& blockMask := by
  dsimp [swapOracleImage]
  apply Nat.eq_of_testBit_eq
  intro i
  simp only [Nat.testBit_and]
  by_cases hi : i < p.n
  · have hmask : ((1 <<< p.n) - 1).testBit i = true := by
      rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]
      simp [hi]
    have hnle : ¬p.n ≤ i := Nat.not_le_of_gt hi
    simp only [Nat.testBit_shiftRight, Nat.testBit_xor, Nat.testBit_shiftLeft,
      Nat.testBit_and]
    simp [hmask, hnle, Nat.add_comm, Nat.add_left_comm]
  · have hmask : ((1 <<< p.n) - 1).testBit i = false := by
      rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]
      simp [hi]
    simp [hmask]

/--
SWAP proof-DAG block: after `swapOracleImage`, the high n-bit register equals
the old low n-bit register.  This is the symmetric register equation paired
with `swapOracleImage_block1_eq_block2`; it is still only a bit-slice block,
not a SWAP unitarity proof.
main.tex:1140 --/
theorem swapOracleImage_block2_eq_block1 (p : OneTermRobinParameters) (j : Nat) :
    let n := p.n
    let blockMask := (1 <<< n) - 1
    ((swapOracleImage p j) >>> (1 + n)) &&& blockMask =
      (j >>> 1) &&& blockMask := by
  dsimp [swapOracleImage]
  apply Nat.eq_of_testBit_eq
  intro i
  simp only [Nat.testBit_and]
  by_cases hi : i < p.n
  · have hmask : ((1 <<< p.n) - 1).testBit i = true := by
      rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]
      simp [hi]
    have hmaskHigh : ((1 <<< p.n) - 1).testBit (i + p.n) = false := by
      rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]
      have hle : p.n ≤ i + p.n := by omega
      simp [Nat.not_lt.mpr hle]
    have hshift : 1 ≤ i + (p.n + 1) := by omega
    simp only [Nat.testBit_shiftRight, Nat.testBit_xor, Nat.testBit_shiftLeft,
      Nat.testBit_and]
    simp [hmask, hmaskHigh, hshift, Nat.add_comm, Nat.add_left_comm, Nat.add_assoc]
    by_cases hlow : j.testBit (i + 1)
    · by_cases hhigh : j.testBit (i + (p.n + 1)) <;> simp [hlow, hhigh]
    · by_cases hhigh : j.testBit (i + (p.n + 1)) <;> simp [hlow, hhigh]
  · have hmask : ((1 <<< p.n) - 1).testBit i = false := by
      rw [Nat.one_shiftLeft, Nat.testBit_two_pow_sub_one]
      simp [hi]
    simp [hmask]

/--
SWAP proof-DAG block: the XOR difference between the two exchanged registers is
preserved by one SWAP application.  This uses only the two register block
equations and is independent of any gate unitarity flag.
-/
theorem swapOracleDiff_preserved (p : OneTermRobinParameters) (j : Nat) :
    swapOracleDiff p (swapOracleImage p j) = swapOracleDiff p j := by
  unfold swapOracleDiff
  dsimp
  rw [swapOracleImage_block1_eq_block2 p j,
    swapOracleImage_block2_eq_block1 p j]
  exact Nat.xor_comm _ _

/-- XORing the same two shifted masks twice cancels them bitwise. -/
theorem xor_two_shifted_masks_cancel (j diff n : Nat) :
    (j ^^^ (diff <<< 1) ^^^ (diff <<< (1 + n))) ^^^
        (diff <<< 1) ^^^ (diff <<< (1 + n)) = j := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp only [Nat.testBit_xor]
  cases hj : j.testBit i <;>
    cases hlow : (diff <<< 1).testBit i <;>
    cases hhigh : (diff <<< (1 + n)).testBit i <;>
    rfl

/--
SWAP proof-DAG block: the image function is self-inverse.

This is the arithmetic image fact reused by the finite permutation-matrix
bridge.
-/
theorem swapOracleImage_self_inverse (p : OneTermRobinParameters) (j : Nat) :
    swapOracleImage p (swapOracleImage p j) = j := by
  rw [swapOracleImage_eq_xor_diff p (swapOracleImage p j)]
  rw [swapOracleDiff_preserved p j]
  rw [swapOracleImage_eq_xor_diff p j]
  exact xor_two_shifted_masks_cancel j (swapOracleDiff p j) p.n

/--
SWAP proof-DAG block: injectivity of the image function, derived from the
self-inverse arithmetic block without opening the bit-slice proof again.
-/
theorem swapOracleImage_injective (p : OneTermRobinParameters) {j₁ j₂ : Nat}
    (h : swapOracleImage p j₁ = swapOracleImage p j₂) :
    j₁ = j₂ := by
  have h1 := swapOracleImage_self_inverse p j₁
  have h2 := swapOracleImage_self_inverse p j₂
  rw [← h1, ← h2, h]

/--
SWAP proof-DAG block: bijectivity of `swapOracleImage` on the finite full
Hilbert-space basis.

The finite map uses `swapOracleImage_lt_qubitDim` for the `Fin` constructor and
`swapOracleImage_self_inverse` for both injectivity and surjectivity.
-/
theorem swapOracleImage_bijective (p : OneTermRobinParameters) :
    (∀ (a b : Fin (qubitDim (oneTermRobinTotalQubits p))),
        (⟨swapOracleImage p a.val, swapOracleImage_lt_qubitDim p a.2⟩ :
          Fin (qubitDim (oneTermRobinTotalQubits p))) =
        ⟨swapOracleImage p b.val, swapOracleImage_lt_qubitDim p b.2⟩ →
        a = b) ∧
    ∀ (y : Fin (qubitDim (oneTermRobinTotalQubits p))),
      ∃ (x : Fin (qubitDim (oneTermRobinTotalQubits p))),
        (⟨swapOracleImage p x.val, swapOracleImage_lt_qubitDim p x.2⟩ :
          Fin (qubitDim (oneTermRobinTotalQubits p))) = y := by
  constructor
  · intro a b h
    apply Fin.ext
    exact swapOracleImage_injective p (Fin.ext_iff.mp h)
  · intro y
    refine ⟨⟨swapOracleImage p y.val, swapOracleImage_lt_qubitDim p y.2⟩, ?_⟩
    apply Fin.ext
    exact swapOracleImage_self_inverse p y.val

/--
For each SWAP matrix column, the row indexed by `swapOracleImage` contains the
unique `1` entry.
-/
theorem swapOracleMatrix_col_has_one (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    swapOracleMatrix p
      (⟨swapOracleImage p j.val, swapOracleImage_lt_qubitDim p j.2⟩ :
        Fin (qubitDim (oneTermRobinTotalQubits p))) j = Coeff.rat 1 := by
  rw [swapOracleMatrix_eq_image]
  simp

/--
For each SWAP matrix column, any `1` entry must occur at the row indexed by
`swapOracleImage`.
-/
theorem swapOracleMatrix_col_unique (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (h : swapOracleMatrix p i j = Coeff.rat 1) :
    i = ⟨swapOracleImage p j.val, swapOracleImage_lt_qubitDim p j.2⟩ := by
  rw [swapOracleMatrix_eq_image] at h
  split at h
  · next h_cond => exact Fin.ext h_cond
  · next _ => simp at h

/-- Every SWAP matrix row has a `1` entry, by finite surjectivity. -/
theorem swapOracleMatrix_row_has_one (p : OneTermRobinParameters)
    (i : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    ∃ (j : Fin (qubitDim (oneTermRobinTotalQubits p))),
      swapOracleMatrix p i j = Coeff.rat 1 := by
  have h_surj := (swapOracleImage_bijective p).2 i
  have ⟨⟨xval, xprop⟩, hx⟩ := h_surj
  refine ⟨⟨xval, xprop⟩, ?_⟩
  rw [swapOracleMatrix_eq_image]
  have h_eq : i.val = swapOracleImage p xval := by
    have := Fin.ext_iff.mp hx
    simp at this
    exact this.symm
  simp [h_eq]

/-- Every SWAP matrix row has a unique `1` entry, by finite injectivity. -/
theorem swapOracleMatrix_row_unique (p : OneTermRobinParameters)
    (i : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (j₁ j₂ : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (h₁ : swapOracleMatrix p i j₁ = Coeff.rat 1)
    (h₂ : swapOracleMatrix p i j₂ = Coeff.rat 1) :
    j₁ = j₂ := by
  have key₁ := swapOracleMatrix_col_unique p i j₁ h₁
  have key₂ := swapOracleMatrix_col_unique p i j₂ h₂
  have h_inj := (swapOracleImage_bijective p).1
  exact h_inj j₁ j₂ (key₁.symm.trans key₂)

/--
SWAP matrix is a finite permutation matrix: every row and column has exactly
one entry equal to `1`.

This closes the SWAP gate-level matrix-semantics bridge while leaving the
paper-specific O_D^BS, O_f, LCU, and block-extraction obligations unchanged.
-/
theorem swapOracleMatrix_is_permutation (p : OneTermRobinParameters) :
    (∀ (i : Fin (qubitDim (oneTermRobinTotalQubits p))),
      ∃ (j : Fin (qubitDim (oneTermRobinTotalQubits p))),
        swapOracleMatrix p i j = Coeff.rat 1 ∧
        ∀ (j' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          swapOracleMatrix p i j' = Coeff.rat 1 → j' = j) ∧
    (∀ (j : Fin (qubitDim (oneTermRobinTotalQubits p))),
      ∃ (i : Fin (qubitDim (oneTermRobinTotalQubits p))),
        swapOracleMatrix p i j = Coeff.rat 1 ∧
        ∀ (i' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          swapOracleMatrix p i' j = Coeff.rat 1 → i' = i) := by
  constructor
  · intro i
    have ⟨j, hj⟩ := swapOracleMatrix_row_has_one p i
    exact ⟨j, hj, fun j' hj' => (swapOracleMatrix_row_unique p i j j' hj hj').symm⟩
  · intro j
    let row := (⟨swapOracleImage p j.val, swapOracleImage_lt_qubitDim p j.2⟩ :
                  Fin (qubitDim (oneTermRobinTotalQubits p)))
    exact ⟨row, swapOracleMatrix_col_has_one p j,
      fun i' hi' => swapOracleMatrix_col_unique p i' j hi'⟩

/--
After the active Lemma 1 paper image and the SWAP gate, the system-row register
contains the paper address `r_si`.  This is a post-SWAP register equation under
the same n-bit address hypothesis used by the finite image bridge; it does not
construct a dagger preimage or promote cleanup.
-/
theorem bandedSparseAccessPaperPostSwap_rowValue_eq_address
    (p : OneTermRobinParameters) (j : Nat)
    (haddr : bandedSparseAccessPaperAddress p j < (1 <<< p.n)) :
    (bandedSparseAccessPaperRegisters p
      (swapOracleImage p (bandedSparseAccessPaperImage p j))).rowValue =
      bandedSparseAccessPaperAddress p j := by
  have hswap :=
    swapOracleImage_block1_eq_block2 p (bandedSparseAccessPaperImage p j)
  have himage := bandedSparseAccessPaperImage_odRegisterValue_eq p j haddr
  unfold bandedSparseAccessPaperRegisters at hswap himage ⊢
  simpa using hswap.trans himage

/--
After the active Lemma 1 paper image and the SWAP gate, the O_D register
contains the original row value.  This is the second post-SWAP register
equation needed before inverse-on-range cleanup search.
-/
theorem bandedSparseAccessPaperPostSwap_odRegisterValue_eq_rowValue
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessPaperRegisters p
      (swapOracleImage p (bandedSparseAccessPaperImage p j))).odRegisterValue =
      (bandedSparseAccessPaperRegisters p j).rowValue := by
  have hswap :=
    swapOracleImage_block2_eq_block1 p (bandedSparseAccessPaperImage p j)
  have himage := bandedSparseAccessPaperImage_rowValue_eq p j
  unfold bandedSparseAccessPaperRegisters at hswap himage ⊢
  simpa using hswap.trans himage

/--
After the active paper image and SWAP, the post-SWAP column is still a finite
basis index whenever the source column is finite and the written paper address
is n-bit.  This does not prove inverse-on-range or cleanup.
-/
theorem bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (haddr : bandedSparseAccessPaperAddress p source.val < (1 <<< p.n)) :
    swapOracleImage p (bandedSparseAccessPaperImage p source.val) <
      qubitDim (oneTermRobinTotalQubits p) := by
  have himage :
      bandedSparseAccessPaperImage p source.val <
        qubitDim (oneTermRobinTotalQubits p) :=
    bandedSparseAccessPaperImage_lt_qubitDim_of_address_lt
      p source.val source.2 haddr
  exact swapOracleImage_lt_qubitDim p himage

/--
Replace the `O_D^BS` n-bit register of a compound index while preserving the
low ancilla/system block and all high-tail bits.

This is the local splice used to build a post-SWAP cleanup preimage candidate.
It does not assert that the chosen `odValue` is the correct reverse address.
-/
def bandedSparseAccessPaperSpliceODRegister
    (p : OneTermRobinParameters) (j odValue : Nat) : Nat :=
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  j % lowBase + odValue * lowBase + (j / highBase) * highBase

/-- The paper image is the O_D-register splice with the computed paper address. -/
theorem bandedSparseAccessPaperImage_eq_splice
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperImage p j =
      bandedSparseAccessPaperSpliceODRegister p j
        (bandedSparseAccessPaperAddress p j) := by
  rfl

/-- The spliced low-and-O_D block fits below the high-tail boundary for n-bit O_D values. -/
theorem bandedSparseAccessPaperSpliceODRegister_lowBlock_lt_highBase_of_odValue_lt
    (p : OneTermRobinParameters) (j odValue : Nat)
    (hod : odValue < (1 <<< p.n)) :
    let lowWidth := 1 + p.n
    let highWidth := 1 + 2 * p.n
    let lowBase := 2 ^ lowWidth
    let highBase := 2 ^ highWidth
    let lowPrefix := j % lowBase
    lowPrefix + odValue * lowBase < highBase := by
  rw [Nat.one_shiftLeft] at hod
  dsimp
  have hlowPos : 0 < 2 ^ (1 + p.n) :=
    Nat.pow_pos (by decide : 0 < 2)
  have hlow : j % 2 ^ (1 + p.n) < 2 ^ (1 + p.n) :=
    Nat.mod_lt j hlowPos
  have hbase : 2 ^ (1 + 2 * p.n) = 2 ^ (1 + p.n) * 2 ^ p.n := by
    rw [← Nat.pow_add]
    congr 1
    omega
  rw [hbase]
  have hlt1 :
      j % 2 ^ (1 + p.n) + odValue * 2 ^ (1 + p.n) <
        2 ^ (1 + p.n) + odValue * 2 ^ (1 + p.n) := by
    exact Nat.add_lt_add_right hlow (odValue * 2 ^ (1 + p.n))
  have hsucc : odValue + 1 ≤ 2 ^ p.n := Nat.succ_le_of_lt hod
  have hle :
      (odValue + 1) * 2 ^ (1 + p.n) ≤ 2 ^ p.n * 2 ^ (1 + p.n) := by
    exact Nat.mul_le_mul_right (2 ^ (1 + p.n)) hsucc
  have heq :
      2 ^ (1 + p.n) + odValue * 2 ^ (1 + p.n) =
        (odValue + 1) * 2 ^ (1 + p.n) := by
    rw [Nat.add_comm]
    exact (Nat.succ_mul odValue (2 ^ (1 + p.n))).symm
  rw [heq] at hlt1
  rw [Nat.mul_comm (2 ^ (1 + p.n)) (2 ^ p.n)]
  exact Nat.lt_of_lt_of_le hlt1 hle

/-- Splicing an O_D value preserves the low ancilla-and-row block. -/
theorem bandedSparseAccessPaperSpliceODRegister_mod_lowBase
    (p : OneTermRobinParameters) (j odValue : Nat) :
    bandedSparseAccessPaperSpliceODRegister p j odValue % 2 ^ (1 + p.n) =
      j % 2 ^ (1 + p.n) := by
  unfold bandedSparseAccessPaperSpliceODRegister
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  have hbase : highBase = lowBase * 2 ^ p.n := by
    dsimp [highBase, lowBase, highWidth, lowWidth]
    rw [← Nat.pow_add]
    congr 1
    omega
  have hlow : lowPrefix % lowBase = lowPrefix := by
    dsimp [lowPrefix]
    exact Nat.mod_eq_of_lt (Nat.mod_lt j (Nat.pow_pos (by decide : 0 < 2)))
  calc
    (lowPrefix + odValue * lowBase + j / highBase * highBase) % lowBase
        = (lowPrefix + lowBase * odValue + j / highBase * highBase) % lowBase := by
          rw [Nat.mul_comm odValue lowBase]
    _ = (lowPrefix + lowBase * odValue + j / highBase * (lowBase * 2 ^ p.n)) %
          lowBase := by
          rw [hbase]
    _ = (lowPrefix + lowBase * (odValue + j / highBase * 2 ^ p.n)) % lowBase := by
          congr 1
          rw [Nat.mul_add]
          ac_rfl
    _ = lowPrefix % lowBase := by
          rw [Nat.add_mul_mod_self_left]
    _ = lowPrefix := hlow
    _ = j % 2 ^ (1 + p.n) := by rfl

/-- Splicing an n-bit O_D value exposes that value when the O_D register is extracted. -/
theorem bandedSparseAccessPaperSpliceODRegister_div_lowBase_mod_eq
    (p : OneTermRobinParameters) (j odValue : Nat)
    (hod : odValue < (1 <<< p.n)) :
    bandedSparseAccessPaperSpliceODRegister p j odValue / 2 ^ (1 + p.n) %
        2 ^ p.n =
      odValue := by
  unfold bandedSparseAccessPaperSpliceODRegister
  rw [Nat.one_shiftLeft] at hod
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  have hlowPos : 0 < lowBase := by
    dsimp [lowBase, lowWidth]
    exact Nat.pow_pos (by decide : 0 < 2)
  have hlow : lowPrefix < lowBase := by
    dsimp [lowPrefix]
    exact Nat.mod_lt j hlowPos
  have hbase : highBase = lowBase * 2 ^ p.n := by
    dsimp [highBase, lowBase, highWidth, lowWidth]
    rw [← Nat.pow_add]
    congr 1
    omega
  have hsplice : lowPrefix + odValue * lowBase + j / highBase * highBase =
      lowPrefix + lowBase * (odValue + j / highBase * 2 ^ p.n) := by
    rw [hbase]
    rw [Nat.mul_add]
    ac_rfl
  have hdiv :
      (lowPrefix + lowBase * (odValue + j / highBase * 2 ^ p.n)) / lowBase =
        odValue + j / highBase * 2 ^ p.n := by
    rw [Nat.add_mul_div_left _ _ hlowPos]
    rw [Nat.div_eq_of_lt hlow]
    simp
  have hlowWidth : 2 ^ (1 + p.n) = lowBase := by rfl
  rw [hlowWidth]
  rw [hsplice]
  rw [hdiv]
  rw [Nat.add_mul_mod_self_right]
  exact Nat.mod_eq_of_lt hod

/-- Splicing preserves the row field. -/
theorem bandedSparseAccessPaperSpliceODRegister_rowValue_eq
    (p : OneTermRobinParameters) (j odValue : Nat) :
    (bandedSparseAccessPaperRegisters p
      (bandedSparseAccessPaperSpliceODRegister p j odValue)).rowValue =
      (bandedSparseAccessPaperRegisters p j).rowValue := by
  unfold bandedSparseAccessPaperRegisters
  simp only []
  rw [bandedSparseAccessPaperRegisterValue_eq_mod,
    bandedSparseAccessPaperRegisterValue_eq_mod]
  have hpow : 2 * 2 ^ p.n = 2 ^ (1 + p.n) := by
    rw [show 1 + p.n = p.n + 1 by omega, Nat.pow_succ]
    omega
  have hmod := bandedSparseAccessPaperSpliceODRegister_mod_lowBase p j odValue
  rw [← hpow] at hmod
  rw [← Nat.mod_mul_right_div_self
    (bandedSparseAccessPaperSpliceODRegister p j odValue) 2 (2 ^ p.n)]
  rw [← Nat.mod_mul_right_div_self j 2 (2 ^ p.n)]
  rw [hmod]

/-- Splicing an n-bit value into the O_D block makes that value the extracted O_D register. -/
theorem bandedSparseAccessPaperSpliceODRegister_odRegisterValue_eq
    (p : OneTermRobinParameters) (j odValue : Nat)
    (hod : odValue < (1 <<< p.n)) :
    (bandedSparseAccessPaperRegisters p
      (bandedSparseAccessPaperSpliceODRegister p j odValue)).odRegisterValue =
      odValue := by
  unfold bandedSparseAccessPaperRegisters
  simp only []
  rw [bandedSparseAccessPaperRegisterValue_eq_mod]
  exact bandedSparseAccessPaperSpliceODRegister_div_lowBase_mod_eq p j odValue hod

/-- Splicing an n-bit O_D value preserves all bits above the O_D register. -/
theorem bandedSparseAccessPaperSpliceODRegister_div_highBase_eq_of_odValue_lt
    (p : OneTermRobinParameters) (j odValue : Nat)
    (hod : odValue < (1 <<< p.n)) :
    bandedSparseAccessPaperSpliceODRegister p j odValue / 2 ^ (1 + 2 * p.n) =
      j / 2 ^ (1 + 2 * p.n) := by
  unfold bandedSparseAccessPaperSpliceODRegister
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  have hhighPos : 0 < highBase := by
    dsimp [highBase, highWidth]
    exact Nat.pow_pos (by decide : 0 < 2)
  have hsmall : lowPrefix + odValue * lowBase < highBase :=
    bandedSparseAccessPaperSpliceODRegister_lowBlock_lt_highBase_of_odValue_lt
      p j odValue hod
  calc
    (lowPrefix + odValue * lowBase + j / highBase * highBase) / highBase
        = (lowPrefix + odValue * lowBase + highBase * (j / highBase)) /
            highBase := by
          rw [Nat.mul_comm (j / highBase) highBase]
    _ = (lowPrefix + odValue * lowBase) / highBase + j / highBase := by
          rw [Nat.add_mul_div_left _ _ hhighPos]
    _ = j / highBase := by simp [Nat.div_eq_of_lt hsmall]
    _ = j / 2 ^ (1 + 2 * p.n) := by rfl

/--
Splicing an n-bit O_D value into a finite compound basis index preserves the
full finite-basis range.  This is the range counterpart of the splice register
equations and does not assert that the chosen O_D value is semantically correct.
-/
theorem bandedSparseAccessPaperSpliceODRegister_lt_qubitDim_of_odValue_lt
    (p : OneTermRobinParameters) (j odValue : Nat)
    (hj : j < qubitDim (oneTermRobinTotalQubits p))
    (hod : odValue < (1 <<< p.n)) :
    bandedSparseAccessPaperSpliceODRegister p j odValue <
      qubitDim (oneTermRobinTotalQubits p) := by
  simp only [qubitDim, gridSize] at hj ⊢
  unfold bandedSparseAccessPaperSpliceODRegister
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let highBase := 2 ^ highWidth
  let lowPrefix := j % lowBase
  have hsmall :
      lowPrefix + odValue * lowBase < highBase :=
    bandedSparseAccessPaperSpliceODRegister_lowBlock_lt_highBase_of_odValue_lt
      p j odValue hod
  have hwidth : highWidth ≤ oneTermRobinTotalQubits p := by
    dsimp [highWidth]
    exact bandedSparseAccessPaperHighWidth_le_totalQubits p
  have hpowTotal : highBase * 2 ^ (oneTermRobinTotalQubits p - highWidth) =
      2 ^ oneTermRobinTotalQubits p := by
    dsimp [highBase]
    rw [← Nat.pow_add]
    congr 1
    omega
  have htail_lt : j / highBase < 2 ^ (oneTermRobinTotalQubits p - highWidth) := by
    apply Nat.div_lt_of_lt_mul
    rwa [hpowTotal]
  have htail_succ :
      j / highBase + 1 ≤ 2 ^ (oneTermRobinTotalQubits p - highWidth) :=
    Nat.succ_le_of_lt htail_lt
  have hblock :
      lowPrefix + odValue * lowBase + j / highBase * highBase <
        highBase * (j / highBase + 1) := by
    rw [Nat.mul_succ, Nat.mul_comm highBase (j / highBase)]
    omega
  have htotal :
      highBase * (j / highBase + 1) ≤ 2 ^ oneTermRobinTotalQubits p := by
    have hmul := Nat.mul_le_mul_left highBase htail_succ
    rwa [hpowTotal] at hmul
  exact Nat.lt_of_lt_of_le hblock htotal

/-- Replacing the O_D block twice is the same as keeping the second replacement. -/
theorem bandedSparseAccessPaperSpliceODRegister_splice_of_odValue_lt
    (p : OneTermRobinParameters) (j odValue newODValue : Nat)
    (hod : odValue < (1 <<< p.n)) :
    bandedSparseAccessPaperSpliceODRegister p
        (bandedSparseAccessPaperSpliceODRegister p j odValue) newODValue =
      bandedSparseAccessPaperSpliceODRegister p j newODValue := by
  have hmod := bandedSparseAccessPaperSpliceODRegister_mod_lowBase p j odValue
  have hdiv :=
    bandedSparseAccessPaperSpliceODRegister_div_highBase_eq_of_odValue_lt
      p j odValue hod
  unfold bandedSparseAccessPaperSpliceODRegister at hmod hdiv ⊢
  simp only [] at hmod hdiv ⊢
  rw [hmod, hdiv]

/-- Reconstructing an index from its low, O_D, and high blocks gives the same index. -/
theorem bandedSparseAccessPaperSpliceODRegister_self
    (p : OneTermRobinParameters) (j : Nat) :
    bandedSparseAccessPaperSpliceODRegister p j
      (bandedSparseAccessPaperRegisters p j).odRegisterValue = j := by
  unfold bandedSparseAccessPaperSpliceODRegister
  let lowWidth := 1 + p.n
  let highWidth := 1 + 2 * p.n
  let lowBase := 2 ^ lowWidth
  let midBase := 2 ^ p.n
  let highBase := 2 ^ highWidth
  have hbase : highBase = lowBase * midBase := by
    dsimp [highBase, lowBase, midBase, highWidth, lowWidth]
    rw [← Nat.pow_add]
    congr 1
    omega
  have hod : (bandedSparseAccessPaperRegisters p j).odRegisterValue =
      (j / lowBase) % midBase := by
    unfold bandedSparseAccessPaperRegisters
    dsimp [lowBase, midBase, lowWidth]
    rw [bandedSparseAccessPaperRegisterValue_eq_mod]
  have hmodH :
      j % highBase = j % lowBase + ((j / lowBase) % midBase) * lowBase := by
    have hdecomp := Nat.mod_add_div (j % highBase) lowBase
    have hmodLow : j % highBase % lowBase = j % lowBase := by
      rw [hbase]
      exact Nat.mod_mul_right_mod j lowBase midBase
    have hdivMid : j % highBase / lowBase = j / lowBase % midBase := by
      rw [hbase]
      exact Nat.mod_mul_right_div_self j lowBase midBase
    rw [← hdecomp, hmodLow, hdivMid]
    ac_rfl
  calc
    j % lowBase + (bandedSparseAccessPaperRegisters p j).odRegisterValue * lowBase +
          j / highBase * highBase
        = j % lowBase + ((j / lowBase) % midBase) * lowBase +
          j / highBase * highBase := by rw [hod]
    _ = j % highBase + j / highBase * highBase := by rw [hmodH]
    _ = j := by
      rw [Nat.mul_comm (j / highBase) highBase]
      exact Nat.mod_add_div j highBase

/-- Clean `O_D^BS` register value whose padded-low part is zero and sparse part is `sparseValue`. -/
def bandedSparseAccessPaperCleanODValue
    (p : OneTermRobinParameters) (sparseValue : Nat) : Nat :=
  sparseValue <<< (p.n - clog2 p.kappa)

/-- The clean O_D value has zeroes in the padded low slice. -/
theorem bandedSparseAccessPaperCleanODValue_paddedZero_eq_zero
    (p : OneTermRobinParameters) (sparseValue : Nat) :
    bandedSparseAccessPaperCleanODValue p sparseValue &&&
        ((1 <<< (p.n - clog2 p.kappa)) - 1) = 0 := by
  unfold bandedSparseAccessPaperCleanODValue
  exact shiftLeft_land_mask_eq_zero sparseValue (p.n - clog2 p.kappa)
    (p.n - clog2 p.kappa) (by omega)

/-- A clean sparse value fits in the n-bit O_D register when the sparse width fits in n. -/
theorem bandedSparseAccessPaperCleanODValue_lt_two_pow_of_sparse_lt
    (p : OneTermRobinParameters) {sparseValue : Nat}
    (hwidth : clog2 p.kappa ≤ p.n)
    (hsparse : sparseValue < 2 ^ clog2 p.kappa) :
    bandedSparseAccessPaperCleanODValue p sparseValue < (1 <<< p.n) := by
  unfold bandedSparseAccessPaperCleanODValue
  rw [Nat.shiftLeft_eq, Nat.one_shiftLeft]
  have hpow : 2 ^ p.n = 2 ^ clog2 p.kappa * 2 ^ (p.n - clog2 p.kappa) := by
    rw [← Nat.pow_add]
    congr 1
    omega
  rw [hpow]
  exact Nat.mul_lt_mul_of_pos_right hsparse (Nat.pow_pos (by decide : 0 < 2))

/-- Extracting the sparse slice from a clean O_D value recovers the sparse value. -/
theorem bandedSparseAccessPaperCleanODValue_sparseIndex_eq
    (p : OneTermRobinParameters) {sparseValue : Nat}
    (hsparse : sparseValue < 2 ^ clog2 p.kappa) :
    ((bandedSparseAccessPaperCleanODValue p sparseValue >>>
          (p.n - clog2 p.kappa)) &&& ((1 <<< clog2 p.kappa) - 1)) =
      sparseValue := by
  rw [bandedSparseAccessPaperRegisterValue_eq_mod]
  unfold bandedSparseAccessPaperCleanODValue
  rw [Nat.shiftLeft_eq]
  rw [Nat.mul_div_left sparseValue (Nat.pow_pos (by decide : 0 < 2))]
  exact Nat.mod_eq_of_lt hsparse

/--
On a clean Lemma 1 source column, the extracted O_D register is exactly the
canonical clean sparse-register value for its sparse slot.

This is the bit-slice reconstruction block needed to lift address injectivity
to full paper-image injectivity.  It only uses the executable clean-input
predicate; it does not prove any semantic cleanup flag.
-/
theorem bandedSparseAccessPaperCleanInput_odRegisterValue_eq_cleanODValue
    (p : OneTermRobinParameters) (j : Nat)
    (hwidth : clog2 p.kappa ≤ p.n)
    (hclean : bandedSparseAccessPaperCleanInput p j = true) :
    (bandedSparseAccessPaperRegisters p j).odRegisterValue =
      bandedSparseAccessPaperCleanODValue p
        (bandedSparseAccessPaperRegisters p j).sparseIndexValue := by
  let regs := bandedSparseAccessPaperRegisters p j
  let a := p.n - clog2 p.kappa
  let b := clog2 p.kappa
  have hcleanZero : regs.paddedZeroValue = 0 := by
    simpa [regs] using (bandedSparseAccessPaperCleanInput_iff p j).1 hclean
  have hpaddedEq :
      regs.paddedZeroValue =
        regs.odRegisterValue &&& ((1 <<< a) - 1) := by
    simpa [regs, a] using
      bandedSparseAccessPaperRegisters_paddedZeroValue_eq p j
  have hmodMask :
      regs.odRegisterValue &&& ((1 <<< a) - 1) =
        regs.odRegisterValue % 2 ^ a := by
    simpa [Nat.shiftRight_zero] using
      bandedSparseAccessPaperRegisterValue_eq_mod regs.odRegisterValue 0 a
  have hodMod : regs.odRegisterValue % 2 ^ a = 0 := by
    rw [hpaddedEq, hmodMask] at hcleanZero
    exact hcleanZero
  have hsparseMod :
      regs.sparseIndexValue =
        (regs.odRegisterValue / 2 ^ a) % 2 ^ b := by
    rw [bandedSparseAccessPaperRegisters_sparseIndexValue_eq]
    simpa [regs, a, b] using
      bandedSparseAccessPaperRegisterValue_eq_mod regs.odRegisterValue a b
  have hodLt :
      regs.odRegisterValue < 2 ^ p.n := by
    simpa [regs, Nat.one_shiftLeft] using
      bandedSparseAccessPaperRegisters_odRegisterValue_lt p j
  have hpow :
      2 ^ p.n = 2 ^ a * 2 ^ b := by
    dsimp [a, b]
    rw [← Nat.pow_add]
    congr 1
    omega
  have hdivLt :
      regs.odRegisterValue / 2 ^ a < 2 ^ b := by
    apply Nat.div_lt_of_lt_mul
    rwa [← hpow]
  have hsparseEq :
      regs.sparseIndexValue = regs.odRegisterValue / 2 ^ a := by
    rw [hsparseMod]
    exact Nat.mod_eq_of_lt hdivLt
  have hdecomp := Nat.mod_add_div regs.odRegisterValue (2 ^ a)
  calc
    regs.odRegisterValue
        = regs.odRegisterValue % 2 ^ a +
            2 ^ a * (regs.odRegisterValue / 2 ^ a) := hdecomp.symm
    _ = 2 ^ a * (regs.odRegisterValue / 2 ^ a) := by
          simp [hodMod]
    _ = (regs.odRegisterValue / 2 ^ a) * 2 ^ a := by
          rw [Nat.mul_comm]
    _ = regs.sparseIndexValue * 2 ^ a := by
          rw [hsparseEq]
    _ = bandedSparseAccessPaperCleanODValue p regs.sparseIndexValue := by
          simp [bandedSparseAccessPaperCleanODValue, Nat.shiftLeft_eq,
            regs, a]

/--
The corrected active `O_D^BS` paper image is injective on the faithful
global-slot clean source domain.

This is a finite-register proof-DAG block, not a semantic-flag promotion.  It
combines low-prefix preservation, high-tail preservation, the written-address
roundtrip, same-row global-address injectivity, and clean O_D register
reconstruction.  The obligation records for inverse-on-range, dagger cleanup,
and unitarity remain false.
-/
theorem bandedSparseAccessPaperImage_injective_on_globalSlotSource
    (p : OneTermRobinParameters)
    (j₁ j₂ : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 ≤ p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource₁ : bandedSparseAccessPaperGlobalSlotSource p j₁.val = true)
    (hsource₂ : bandedSparseAccessPaperGlobalSlotSource p j₂.val = true)
    (himage :
      bandedSparseAccessPaperImage p j₁.val =
        bandedSparseAccessPaperImage p j₂.val) :
    j₁ = j₂ := by
  have htwo : 2 ≤ p.n := by omega
  have hwidth : clog2 p.kappa ≤ p.n := by
    rw [hκbits]
    omega
  have haddr₁ :
      bandedSparseAccessPaperAddress p j₁.val < (1 <<< p.n) := by
    have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
      p j₁.val htwo
    simpa [gridSize, Nat.one_shiftLeft] using h
  have haddr₂ :
      bandedSparseAccessPaperAddress p j₂.val < (1 <<< p.n) := by
    have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
      p j₂.val htwo
    simpa [gridSize, Nat.one_shiftLeft] using h
  have hlow :
      j₁.val % 2 ^ (1 + p.n) = j₂.val % 2 ^ (1 + p.n) := by
    calc
      j₁.val % 2 ^ (1 + p.n)
          = bandedSparseAccessPaperImage p j₁.val % 2 ^ (1 + p.n) := by
              rw [bandedSparseAccessPaperImage_mod_lowBase]
      _ = bandedSparseAccessPaperImage p j₂.val % 2 ^ (1 + p.n) := by
              rw [himage]
      _ = j₂.val % 2 ^ (1 + p.n) := by
              rw [bandedSparseAccessPaperImage_mod_lowBase]
  have htail :
      bandedSparseAccessPaperHighTail p j₁.val =
        bandedSparseAccessPaperHighTail p j₂.val := by
    calc
      bandedSparseAccessPaperHighTail p j₁.val =
          bandedSparseAccessPaperHighTail p
            (bandedSparseAccessPaperImage p j₁.val) := by
            exact (bandedSparseAccessPaperImage_highTail_eq_of_address_lt
              p j₁.val haddr₁).symm
      _ = bandedSparseAccessPaperHighTail p
            (bandedSparseAccessPaperImage p j₂.val) := by
            rw [himage]
      _ = bandedSparseAccessPaperHighTail p j₂.val :=
            bandedSparseAccessPaperImage_highTail_eq_of_address_lt
              p j₂.val haddr₂
  have htailDiv :
      j₁.val / 2 ^ (1 + 2 * p.n) =
        j₂.val / 2 ^ (1 + 2 * p.n) := by
    simpa [bandedSparseAccessPaperHighTail, Nat.shiftRight_eq_div_pow]
      using htail
  have hrow :
      (bandedSparseAccessPaperRegisters p j₁.val).rowValue =
        (bandedSparseAccessPaperRegisters p j₂.val).rowValue := by
    calc
      (bandedSparseAccessPaperRegisters p j₁.val).rowValue =
          (bandedSparseAccessPaperRegisters p
            (bandedSparseAccessPaperImage p j₁.val)).rowValue := by
            exact (bandedSparseAccessPaperImage_rowValue_eq p j₁.val).symm
      _ = (bandedSparseAccessPaperRegisters p
            (bandedSparseAccessPaperImage p j₂.val)).rowValue := by
            rw [himage]
      _ = (bandedSparseAccessPaperRegisters p j₂.val).rowValue :=
            bandedSparseAccessPaperImage_rowValue_eq p j₂.val
  have haddrEq :
      bandedSparseAccessPaperAddress p j₁.val =
        bandedSparseAccessPaperAddress p j₂.val := by
    calc
      bandedSparseAccessPaperAddress p j₁.val =
          (bandedSparseAccessPaperRegisters p
            (bandedSparseAccessPaperImage p j₁.val)).odRegisterValue := by
            exact (bandedSparseAccessPaperImage_odRegisterValue_eq
              p j₁.val haddr₁).symm
      _ = (bandedSparseAccessPaperRegisters p
            (bandedSparseAccessPaperImage p j₂.val)).odRegisterValue := by
            rw [himage]
      _ = bandedSparseAccessPaperAddress p j₂.val :=
            bandedSparseAccessPaperImage_odRegisterValue_eq p j₂.val haddr₂
  have hsparse :
      (bandedSparseAccessPaperRegisters p j₁.val).sparseIndexValue =
        (bandedSparseAccessPaperRegisters p j₂.val).sparseIndexValue :=
    bandedSparseAccessPaperAddress_same_row_injective_of_globalSlotSource
      p hn hkappa hsource₁ hsource₂ hrow haddrEq
  have hclean₁ :
      bandedSparseAccessPaperCleanInput p j₁.val = true :=
    bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
      p j₁.val hsource₁
  have hclean₂ :
      bandedSparseAccessPaperCleanInput p j₂.val = true :=
    bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
      p j₂.val hsource₂
  have hod₁ :=
    bandedSparseAccessPaperCleanInput_odRegisterValue_eq_cleanODValue
      p j₁.val hwidth hclean₁
  have hod₂ :=
    bandedSparseAccessPaperCleanInput_odRegisterValue_eq_cleanODValue
      p j₂.val hwidth hclean₂
  have hod :
      (bandedSparseAccessPaperRegisters p j₁.val).odRegisterValue =
        (bandedSparseAccessPaperRegisters p j₂.val).odRegisterValue := by
    calc
      (bandedSparseAccessPaperRegisters p j₁.val).odRegisterValue =
          bandedSparseAccessPaperCleanODValue p
            (bandedSparseAccessPaperRegisters p j₁.val).sparseIndexValue := hod₁
      _ = bandedSparseAccessPaperCleanODValue p
            (bandedSparseAccessPaperRegisters p j₂.val).sparseIndexValue := by
            rw [hsparse]
      _ = (bandedSparseAccessPaperRegisters p j₂.val).odRegisterValue := hod₂.symm
  apply Fin.ext
  calc
    j₁.val =
        bandedSparseAccessPaperSpliceODRegister p j₁.val
          (bandedSparseAccessPaperRegisters p j₁.val).odRegisterValue := by
          exact (bandedSparseAccessPaperSpliceODRegister_self p j₁.val).symm
    _ = bandedSparseAccessPaperSpliceODRegister p j₂.val
          (bandedSparseAccessPaperRegisters p j₂.val).odRegisterValue := by
          simp [bandedSparseAccessPaperSpliceODRegister, hlow, hod, htailDiv]
    _ = j₂.val :=
          bandedSparseAccessPaperSpliceODRegister_self p j₂.val

/--
The reverse sparse index used by the post-SWAP cleanup candidate fits in the
three-bit sparse register for the one-term Robin parameter family.
-/
theorem bandedSparseAccessPaperPostSwapReverseSparse_lt_two_pow
    (p : OneTermRobinParameters) (source : Nat)
    (hn : 3 ≤ p.n) (hκbits : clog2 p.kappa = 3) :
    oneTermRobinGlobalSparseInverseSlot
        (bandedSparseAccessPaperRegisters p source).sparseIndexValue <
      2 ^ clog2 p.kappa := by
  have _nLower := hn
  let regs := bandedSparseAccessPaperRegisters p source
  rw [hκbits]
  exact oneTermRobinGlobalSparseInverseSlot_lt_eight regs.sparseIndexValue

/--
The clean O_D register value spliced into the post-SWAP preimage candidate is
n-bit for the one-term Robin parameter family.
-/
theorem bandedSparseAccessPaperPostSwapCleanODValue_lt_two_pow
    (p : OneTermRobinParameters) (source : Nat)
    (hn : 3 ≤ p.n) (hκbits : clog2 p.kappa = 3) :
    bandedSparseAccessPaperCleanODValue p
        (oneTermRobinGlobalSparseInverseSlot
          (bandedSparseAccessPaperRegisters p source).sparseIndexValue) <
      (1 <<< p.n) := by
  have hreverse :
      oneTermRobinGlobalSparseInverseSlot
          (bandedSparseAccessPaperRegisters p source).sparseIndexValue <
        2 ^ clog2 p.kappa :=
    bandedSparseAccessPaperPostSwapReverseSparse_lt_two_pow
      p source hn hκbits
  have hwidth : clog2 p.kappa ≤ p.n := by
    rw [hκbits]
    omega
  exact bandedSparseAccessPaperCleanODValue_lt_two_pow_of_sparse_lt
    p hwidth hreverse

/--
Candidate clean preimage for the column reached by
`O_D^BS`, SWAP, and then `(O_D^BS)^dagger`.

The candidate keeps the post-SWAP row and high-tail bits, and replaces the
`O_D^BS` register by a clean padded register whose sparse field is the inverse
global slot for the original source slot.  The separate Boolean audit below
checks whether this candidate is actually a paper-image preimage.
-/
def bandedSparseAccessPaperPostSwapPreimageCandidate
    (p : OneTermRobinParameters) (source : Nat) : Nat :=
  let regs := bandedSparseAccessPaperRegisters p source
  let post := swapOracleImage p (bandedSparseAccessPaperImage p source)
  let reverseSparse := oneTermRobinGlobalSparseInverseSlot regs.sparseIndexValue
  bandedSparseAccessPaperSpliceODRegister p post
    (bandedSparseAccessPaperCleanODValue p reverseSparse)

/--
Executable audit for the post-SWAP preimage candidate.

It checks three local facts: the candidate maps by the active paper-image
skeleton to the post-SWAP column, the candidate is in the clean padded domain,
and the candidate address is n-bit.  Even when this Boolean is true for a
finite parameter scan, the paper-level dagger cleanup and unitarity flags
remain unproved.
-/
def bandedSparseAccessPaperPostSwapPreimageCandidateChecks
    (p : OneTermRobinParameters) (source : Nat) : Bool :=
  let post := swapOracleImage p (bandedSparseAccessPaperImage p source)
  let pre := bandedSparseAccessPaperPostSwapPreimageCandidate p source
  (bandedSparseAccessPaperImage p pre == post) &&
    bandedSparseAccessPaperCleanInput p pre &&
    bandedSparseAccessPaperAddressInRange p pre

/--
The post-SWAP preimage candidate passes the executable image, clean-domain, and
address-range checks for clean one-term Robin source columns.

The assumptions keep the current Phase 1 contract explicit: the source column is
in the finite basis, the source padded register is clean, and the one-term
family uses a three-bit sparse register (`kappa = 7`, `clog2 kappa = 3`).  This
does not prove uniqueness, dagger cleanup, unitarity, or block extraction.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_cleanSource
    (p : OneTermRobinParameters) (source : Nat)
    (hn : 3 ≤ p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : source < qubitDim (oneTermRobinTotalQubits p))
    (hclean : bandedSparseAccessPaperCleanInput p source = true) :
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks p source = true := by
  have _sourceFinite := hsource
  have _sourceClean := (bandedSparseAccessPaperCleanInput_iff p source).1 hclean
  have _kappaValue := hkappa
  let regs := bandedSparseAccessPaperRegisters p source
  let post := swapOracleImage p (bandedSparseAccessPaperImage p source)
  let reverseSparse := oneTermRobinGlobalSparseInverseSlot regs.sparseIndexValue
  let cleanOD := bandedSparseAccessPaperCleanODValue p reverseSparse
  let pre := bandedSparseAccessPaperPostSwapPreimageCandidate p source
  have htwo : 2 ≤ p.n := by omega
  have haddrSource : bandedSparseAccessPaperAddress p source < (1 <<< p.n) := by
    have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le p source htwo
    simpa [gridSize, Nat.one_shiftLeft] using h
  have hsourceSparsePow : regs.sparseIndexValue < 2 ^ clog2 p.kappa := by
    have h := bandedSparseAccessPaperRegisters_sparseIndex_lt p source
    rw [Nat.one_shiftLeft] at h
    simpa [regs] using h
  have hsourceSparseLt8 : regs.sparseIndexValue < 8 := by
    have h := hsourceSparsePow
    rw [hκbits] at h
    simpa using h
  have hrowLt : regs.rowValue < gridSize p.n := by
    simpa [regs] using bandedSparseAccessPaperRegisters_row_lt_gridSize p source
  have hreverseLt8 : reverseSparse < 8 := by
    simpa [reverseSparse] using
      oneTermRobinGlobalSparseInverseSlot_lt_eight regs.sparseIndexValue
  have hreversePow : reverseSparse < 2 ^ clog2 p.kappa := by
    rw [hκbits]
    simpa using hreverseLt8
  have hwidth : clog2 p.kappa ≤ p.n := by
    rw [hκbits]
    omega
  have hcleanODBound : cleanOD < (1 <<< p.n) :=
    bandedSparseAccessPaperCleanODValue_lt_two_pow_of_sparse_lt p hwidth hreversePow
  have hpre_eq : pre = bandedSparseAccessPaperSpliceODRegister p post cleanOD := by
    simp [pre, bandedSparseAccessPaperPostSwapPreimageCandidate, post,
      cleanOD, reverseSparse, regs]
  have hpreRow : (bandedSparseAccessPaperRegisters p pre).rowValue =
      (bandedSparseAccessPaperRegisters p post).rowValue := by
    rw [hpre_eq]
    exact bandedSparseAccessPaperSpliceODRegister_rowValue_eq p post cleanOD
  have hpreOD : (bandedSparseAccessPaperRegisters p pre).odRegisterValue = cleanOD := by
    rw [hpre_eq]
    exact bandedSparseAccessPaperSpliceODRegister_odRegisterValue_eq
      p post cleanOD hcleanODBound
  have hpreSparse :
      (bandedSparseAccessPaperRegisters p pre).sparseIndexValue = reverseSparse := by
    rw [bandedSparseAccessPaperRegisters_sparseIndexValue_eq]
    rw [hpreOD]
    exact bandedSparseAccessPaperCleanODValue_sparseIndex_eq p hreversePow
  have hpreClean : bandedSparseAccessPaperCleanInput p pre = true := by
    rw [bandedSparseAccessPaperCleanInput_iff]
    rw [bandedSparseAccessPaperRegisters_paddedZeroValue_eq]
    rw [hpreOD]
    exact bandedSparseAccessPaperCleanODValue_paddedZero_eq_zero p reverseSparse
  have hpreAddressRange : bandedSparseAccessPaperAddressInRange p pre = true :=
    bandedSparseAccessPaperAddressInRange_eq_true_of_two_le p pre htwo
  have hpostRow : (bandedSparseAccessPaperRegisters p post).rowValue =
      bandedSparseAccessPaperAddress p source := by
    dsimp [post]
    exact bandedSparseAccessPaperPostSwap_rowValue_eq_address p source haddrSource
  have hpostOd : (bandedSparseAccessPaperRegisters p post).odRegisterValue =
      regs.rowValue := by
    dsimp [post, regs]
    exact bandedSparseAccessPaperPostSwap_odRegisterValue_eq_rowValue p source
  have hround :
      oneTermRobinGlobalSparseAddress p.n reverseSparse
        (bandedSparseAccessPaperAddress p source) = regs.rowValue := by
    have h :=
      oneTermRobinGlobalSparseAddress_inverseSlot_address_eq
        (n := p.n) (s := regs.sparseIndexValue) (i := regs.rowValue)
        hn hsourceSparseLt8 hrowLt
    simpa [reverseSparse, regs, bandedSparseAccessPaperAddress] using h
  have hroundUnfold :
      oneTermRobinGlobalSparseAddress p.n reverseSparse
        (oneTermRobinGlobalSparseAddress p.n
          (bandedSparseAccessPaperRegisters p source).sparseIndexValue
          (bandedSparseAccessPaperRegisters p source).rowValue) =
        regs.rowValue := by
    simpa [bandedSparseAccessPaperAddress, regs] using hround
  have hpreAddress : bandedSparseAccessPaperAddress p pre =
      (bandedSparseAccessPaperRegisters p post).odRegisterValue := by
    simp [bandedSparseAccessPaperAddress, hpreSparse, hpreRow, hpostRow,
      hroundUnfold, hpostOd]
  have hpreImage : bandedSparseAccessPaperImage p pre = post := by
    rw [bandedSparseAccessPaperImage_eq_splice]
    rw [hpreAddress]
    rw [hpre_eq]
    rw [bandedSparseAccessPaperSpliceODRegister_splice_of_odValue_lt p post cleanOD
      (bandedSparseAccessPaperRegisters p post).odRegisterValue hcleanODBound]
    exact bandedSparseAccessPaperSpliceODRegister_self p post
  change ((bandedSparseAccessPaperImage p pre == post) &&
      bandedSparseAccessPaperCleanInput p pre &&
      bandedSparseAccessPaperAddressInRange p pre) = true
  simp [hpreImage, hpreClean, hpreAddressRange]

/--
The clean post-SWAP preimage candidate is a finite basis index for finite clean
one-term Robin source columns.  This only discharges the `Fin` constructor
premise for the conditional cleanup witness; uniqueness and semantic cleanup
remain open.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_cleanSource
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 ≤ p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hclean : bandedSparseAccessPaperCleanInput p source.val = true) :
    bandedSparseAccessPaperPostSwapPreimageCandidate p source.val <
      qubitDim (oneTermRobinTotalQubits p) := by
  have _kappaValue := hkappa
  have _sourceClean := hclean
  let regs := bandedSparseAccessPaperRegisters p source.val
  let post := swapOracleImage p (bandedSparseAccessPaperImage p source.val)
  let reverseSparse := oneTermRobinGlobalSparseInverseSlot regs.sparseIndexValue
  let cleanOD := bandedSparseAccessPaperCleanODValue p reverseSparse
  let pre := bandedSparseAccessPaperPostSwapPreimageCandidate p source.val
  have htwo : 2 ≤ p.n := by omega
  have haddrSource : bandedSparseAccessPaperAddress p source.val < (1 <<< p.n) := by
    have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
      p source.val htwo
    simpa [gridSize, Nat.one_shiftLeft] using h
  have hpostRange :
      post < qubitDim (oneTermRobinTotalQubits p) := by
    dsimp [post]
    exact bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
      p source haddrSource
  have hcleanODBound : cleanOD < (1 <<< p.n) := by
    dsimp [cleanOD, reverseSparse, regs]
    exact bandedSparseAccessPaperPostSwapCleanODValue_lt_two_pow
      p source.val hn hκbits
  have hpre_eq : pre =
      bandedSparseAccessPaperSpliceODRegister p post cleanOD := by
    simp [pre, bandedSparseAccessPaperPostSwapPreimageCandidate, post,
      cleanOD, reverseSparse, regs]
  have hpreRange :
      pre < qubitDim (oneTermRobinTotalQubits p) := by
    rw [hpre_eq]
    exact bandedSparseAccessPaperSpliceODRegister_lt_qubitDim_of_odValue_lt
      p post cleanOD hpostRange hcleanODBound
  simpa [pre] using hpreRange

/--
Instantiate the conditional post-SWAP cleanup witness with the clean-source
preimage candidate.

The finite `post` and `pre` range facts remain explicit hypotheses.  This
wrapper converts the accepted Boolean candidate audit into the supplied
preimage equality, clean-domain proof, and n-bit address bound required by
`bandedSparseAccessPostSwapCleanup_of_preimage`.  It does not prove finite
range, uniqueness, semantic dagger cleanup, or unitarity.
-/
theorem bandedSparseAccessPostSwapCleanup_of_cleanSourceCandidate
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hclean : bandedSparseAccessPaperCleanInput p source.val = true)
    (hpostRange :
      swapOracleImage p (bandedSparseAccessPaperImage p source.val) <
        qubitDim (oneTermRobinTotalQubits p))
    (hpreRange :
      bandedSparseAccessPaperPostSwapPreimageCandidate p source.val <
        qubitDim (oneTermRobinTotalQubits p)) :
    BandedSparseAccessPostSwapCleanup p source
      ⟨swapOracleImage p (bandedSparseAccessPaperImage p source.val), hpostRange⟩
      ⟨bandedSparseAccessPaperPostSwapPreimageCandidate p source.val, hpreRange⟩ := by
  let postNat := swapOracleImage p (bandedSparseAccessPaperImage p source.val)
  let preNat := bandedSparseAccessPaperPostSwapPreimageCandidate p source.val
  have haudit :=
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_cleanSource
      p source.val hn hkappa hκbits source.2 hclean
  have hparts :
      (bandedSparseAccessPaperImage p preNat == postNat) = true ∧
        bandedSparseAccessPaperCleanInput p preNat = true ∧
        bandedSparseAccessPaperAddressInRange p preNat = true := by
    simpa [bandedSparseAccessPaperPostSwapPreimageCandidateChecks, preNat,
      postNat, Bool.and_assoc] using haudit
  have hpreImage : bandedSparseAccessPaperImage p preNat = postNat :=
    beq_iff_eq.mp hparts.1
  have haddr : bandedSparseAccessPaperAddress p preNat < (1 <<< p.n) :=
    (bandedSparseAccessPaperAddressInRange_iff p preNat).1 hparts.2.2
  exact bandedSparseAccessPostSwapCleanup_of_preimage p source
    ⟨postNat, hpostRange⟩ ⟨preNat, hpreRange⟩
    (by rfl)
    (by simpa [postNat, preNat] using hpreImage.symm)
    hparts.2.1 haddr

/--
Instantiate the clean-source post-SWAP cleanup witness without caller-supplied
finite-range premises.  The theorem only supplies the `Fin` range proofs for
the already conditional candidate witness; it does not prove uniqueness,
dagger cleanup, or either O_D^BS unitarity flag.
-/
theorem bandedSparseAccessPostSwapCleanup_of_cleanSourceCandidate_noRange
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hclean : bandedSparseAccessPaperCleanInput p source.val = true) :
    BandedSparseAccessPostSwapCleanup p source
      ⟨swapOracleImage p (bandedSparseAccessPaperImage p source.val),
        by
          have htwo : 2 ≤ p.n := by omega
          have haddrSource :
              bandedSparseAccessPaperAddress p source.val < (1 <<< p.n) := by
            have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
              p source.val htwo
            simpa [gridSize, Nat.one_shiftLeft] using h
          exact bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
            p source haddrSource⟩
      ⟨bandedSparseAccessPaperPostSwapPreimageCandidate p source.val,
        bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_cleanSource
          p source hn hkappa hκbits hclean⟩ := by
  have htwo : 2 ≤ p.n := by omega
  have haddrSource :
      bandedSparseAccessPaperAddress p source.val < (1 <<< p.n) := by
    have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
      p source.val htwo
    simpa [gridSize, Nat.one_shiftLeft] using h
  have hpostRange :
      swapOracleImage p (bandedSparseAccessPaperImage p source.val) <
        qubitDim (oneTermRobinTotalQubits p) :=
    bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
      p source haddrSource
  have hpreRange :
      bandedSparseAccessPaperPostSwapPreimageCandidate p source.val <
        qubitDim (oneTermRobinTotalQubits p) :=
    bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_cleanSource
      p source hn hkappa hκbits hclean
  exact bandedSparseAccessPostSwapCleanup_of_cleanSourceCandidate
    p source hn hkappa hκbits hclean hpostRange hpreRange

/--
Feed the row-dependent valid-clean-source predicate into the existing
post-SWAP cleanup candidate wrapper.

The predicate `bandedSparseAccessPaperValidCleanSource` is only a Phase 1
source-domain classifier.  This theorem records that it supplies the clean
padded-register hypothesis required by the cleanup candidate.  It does not
prove source-domain completeness, unused-branch unitary extension, preimage
uniqueness, semantic dagger cleanup, or either O_D^BS unitarity flag.
-/
theorem bandedSparseAccessPostSwapCleanup_of_validCleanSourceCandidate_noRange
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hvalid : bandedSparseAccessPaperValidCleanSource p source.val = true) :
    BandedSparseAccessPostSwapCleanup p source
      ⟨swapOracleImage p (bandedSparseAccessPaperImage p source.val),
        by
          have htwo : 2 ≤ p.n := by omega
          have haddrSource :
              bandedSparseAccessPaperAddress p source.val < (1 <<< p.n) := by
            have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
              p source.val htwo
            simpa [gridSize, Nat.one_shiftLeft] using h
          exact bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
            p source haddrSource⟩
      ⟨bandedSparseAccessPaperPostSwapPreimageCandidate p source.val,
        by
          have hclean :
              bandedSparseAccessPaperCleanInput p source.val = true :=
            bandedSparseAccessPaperValidCleanSource_cleanInput_eq_true
              p source.val hvalid
          exact
            bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_cleanSource
              p source hn hkappa hκbits hclean⟩ := by
  have hclean :
      bandedSparseAccessPaperCleanInput p source.val = true :=
    bandedSparseAccessPaperValidCleanSource_cleanInput_eq_true
      p source.val hvalid
  exact bandedSparseAccessPostSwapCleanup_of_cleanSourceCandidate_noRange
    p source hn hkappa hκbits hclean

/--
Feed the faithful global-slot source predicate into the existing post-SWAP
cleanup candidate wrapper.

This is the active-source analogue of the row-dependent valid-clean-source
bridge.  It only extracts the padded clean-input fact from
`bandedSparseAccessPaperGlobalSlotSource` and reuses the conditional cleanup
candidate.  It does not prove preimage uniqueness, semantic dagger cleanup,
unitarity, LCU correctness, or block extraction.
-/
theorem bandedSparseAccessPostSwapCleanup_of_globalSlotSourceCandidate_noRange
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    BandedSparseAccessPostSwapCleanup p source
      ⟨swapOracleImage p (bandedSparseAccessPaperImage p source.val),
        by
          have htwo : 2 ≤ p.n := by omega
          have haddrSource :
              bandedSparseAccessPaperAddress p source.val < (1 <<< p.n) := by
            have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
              p source.val htwo
            simpa [gridSize, Nat.one_shiftLeft] using h
          exact bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
            p source haddrSource⟩
      ⟨bandedSparseAccessPaperPostSwapPreimageCandidate p source.val,
        by
          have hclean :
              bandedSparseAccessPaperCleanInput p source.val = true :=
            bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
              p source.val hsource
          exact
            bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_cleanSource
              p source hn hkappa hκbits hclean⟩ := by
  have hclean :
      bandedSparseAccessPaperCleanInput p source.val = true :=
    bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
      p source.val hsource
  exact bandedSparseAccessPostSwapCleanup_of_cleanSourceCandidate_noRange
    p source hn hkappa hκbits hclean

/--
The post-SWAP preimage candidate audit is available on the active global-slot
source domain.

This is the global-source wrapper around the existing clean-source arithmetic
block.  It proves only the executable candidate check; inverse uniqueness,
semantic dagger cleanup, and unitarity remain separate obligations.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_globalSlotSource
    (p : OneTermRobinParameters) (source : Nat)
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsourceFinite : source < qubitDim (oneTermRobinTotalQubits p))
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source = true) :
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks p source = true := by
  have hclean :
      bandedSparseAccessPaperCleanInput p source = true :=
    bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true p source hsource
  exact bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_cleanSource
    p source hn hkappa hκbits hsourceFinite hclean

/--
The global-source post-SWAP preimage candidate is a finite basis index.

This theorem only names the range premise needed by the conditional cleanup
witness.  It does not prove that the candidate is unique or that the dagger
cleans every in-range image.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_globalSlotSource
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    bandedSparseAccessPaperPostSwapPreimageCandidate p source.val <
      qubitDim (oneTermRobinTotalQubits p) := by
  have hclean :
      bandedSparseAccessPaperCleanInput p source.val = true :=
    bandedSparseAccessPaperGlobalSlotSource_cleanInput_eq_true
      p source.val hsource
  exact bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_cleanSource
    p source hn hkappa hκbits hclean

/--
The post-SWAP preimage candidate has the reverse sparse slot in its extracted
clean O_D register.

This names the splice/sparse-slice calculation used by the cleanup-candidate
audit so the unique-preimage route can reuse it instead of repeating the
bit-level proof.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidate_sparseIndex_eq
    (p : OneTermRobinParameters) (source : Nat)
    (hn : 3 <= p.n) (hκbits : clog2 p.kappa = 3) :
    (bandedSparseAccessPaperRegisters p
      (bandedSparseAccessPaperPostSwapPreimageCandidate p source)).sparseIndexValue =
      oneTermRobinGlobalSparseInverseSlot
        (bandedSparseAccessPaperRegisters p source).sparseIndexValue := by
  let regs := bandedSparseAccessPaperRegisters p source
  let post := swapOracleImage p (bandedSparseAccessPaperImage p source)
  let reverseSparse := oneTermRobinGlobalSparseInverseSlot regs.sparseIndexValue
  let cleanOD := bandedSparseAccessPaperCleanODValue p reverseSparse
  let pre := bandedSparseAccessPaperPostSwapPreimageCandidate p source
  have hreverseLt8 : reverseSparse < 8 := by
    simpa [reverseSparse] using
      oneTermRobinGlobalSparseInverseSlot_lt_eight regs.sparseIndexValue
  have hreversePow : reverseSparse < 2 ^ clog2 p.kappa := by
    rw [hκbits]
    simpa using hreverseLt8
  have hwidth : clog2 p.kappa <= p.n := by
    rw [hκbits]
    omega
  have hcleanODBound : cleanOD < (1 <<< p.n) :=
    bandedSparseAccessPaperCleanODValue_lt_two_pow_of_sparse_lt
      p hwidth hreversePow
  have hpre_eq : pre =
      bandedSparseAccessPaperSpliceODRegister p post cleanOD := by
    simp [pre, bandedSparseAccessPaperPostSwapPreimageCandidate, post,
      cleanOD, reverseSparse, regs]
  have hpreOD :
      (bandedSparseAccessPaperRegisters p pre).odRegisterValue = cleanOD := by
    rw [hpre_eq]
    exact bandedSparseAccessPaperSpliceODRegister_odRegisterValue_eq
      p post cleanOD hcleanODBound
  rw [bandedSparseAccessPaperRegisters_sparseIndexValue_eq]
  rw [hpreOD]
  simpa [reverseSparse, regs] using
    bandedSparseAccessPaperCleanODValue_sparseIndex_eq p hreversePow

/--
The post-SWAP preimage candidate is itself an active global-slot source.

The proof combines the executable candidate audit for clean input with the
named reverse-slot sparse-slice lemma above.  It still does not promote the
inverse-on-range, uniqueness, dagger-cleanup, or unitarity obligation flags.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidate_globalSlotSource_of_globalSlotSource
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    bandedSparseAccessPaperGlobalSlotSource p
      (bandedSparseAccessPaperPostSwapPreimageCandidate p source.val) = true := by
  let pre := bandedSparseAccessPaperPostSwapPreimageCandidate p source.val
  have hchecks :
      bandedSparseAccessPaperPostSwapPreimageCandidateChecks p source.val = true :=
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  have hparts :
      (bandedSparseAccessPaperImage p pre ==
          swapOracleImage p (bandedSparseAccessPaperImage p source.val)) = true ∧
        bandedSparseAccessPaperCleanInput p pre = true ∧
        bandedSparseAccessPaperAddressInRange p pre = true := by
    simpa [bandedSparseAccessPaperPostSwapPreimageCandidateChecks, pre,
      Bool.and_assoc] using hchecks
  have hclean : bandedSparseAccessPaperCleanInput p pre = true := hparts.2.1
  have hsourceSparseLt7 :
      (bandedSparseAccessPaperRegisters p source.val).sparseIndexValue < 7 := by
    have hs :=
      bandedSparseAccessPaperGlobalSlotSource_sparseIndex_lt_kappa
        p source.val hsource
    rwa [hkappa] at hs
  have hreverseLtKappa :
      oneTermRobinGlobalSparseInverseSlot
          (bandedSparseAccessPaperRegisters p source.val).sparseIndexValue <
        p.kappa := by
    rw [hkappa]
    exact oneTermRobinGlobalSparseInverseSlot_lt_seven hsourceSparseLt7
  have hpreSparse :
      (bandedSparseAccessPaperRegisters p pre).sparseIndexValue < p.kappa := by
    rw [bandedSparseAccessPaperPostSwapPreimageCandidate_sparseIndex_eq
      p source.val hn hκbits]
    exact hreverseLtKappa
  simp [bandedSparseAccessPaperGlobalSlotSource,
    bandedSparseAccessPaperSparseIndexInKappa, hclean, hpreSparse, pre]

/--
Uniqueness of the active global-slot clean preimage for the post-SWAP target.

Any active global-source column that maps by the corrected paper image to the
post-SWAP target must be the named reverse-slot preimage candidate.  This is a
finite basis-index lemma for the dagger-cleanup route; semantic obligation
records remain false.
-/
theorem bandedSparseAccessPaperPostSwapPreimageCandidate_unique_on_globalSlotSource
    (p : OneTermRobinParameters)
    (source pre : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true)
    (hpreSource : bandedSparseAccessPaperGlobalSlotSource p pre.val = true)
    (hpreImage :
      bandedSparseAccessPaperImage p pre.val =
        swapOracleImage p (bandedSparseAccessPaperImage p source.val)) :
    pre.val =
      bandedSparseAccessPaperPostSwapPreimageCandidate p source.val := by
  let candVal := bandedSparseAccessPaperPostSwapPreimageCandidate p source.val
  have hcandRange : candVal < qubitDim (oneTermRobinTotalQubits p) := by
    simpa [candVal] using
      bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_globalSlotSource
        p source hn hkappa hκbits hsource
  let cand : Fin (qubitDim (oneTermRobinTotalQubits p)) :=
    ⟨candVal, hcandRange⟩
  have hcandSource :
      bandedSparseAccessPaperGlobalSlotSource p cand.val = true := by
    simpa [cand, candVal] using
      bandedSparseAccessPaperPostSwapPreimageCandidate_globalSlotSource_of_globalSlotSource
        p source hn hkappa hκbits hsource
  have hchecks :
      bandedSparseAccessPaperPostSwapPreimageCandidateChecks p source.val = true :=
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  have hparts :
      (bandedSparseAccessPaperImage p candVal ==
          swapOracleImage p (bandedSparseAccessPaperImage p source.val)) = true ∧
        bandedSparseAccessPaperCleanInput p candVal = true ∧
        bandedSparseAccessPaperAddressInRange p candVal = true := by
    simpa [bandedSparseAccessPaperPostSwapPreimageCandidateChecks, candVal,
      Bool.and_assoc] using hchecks
  have hcandImage :
      bandedSparseAccessPaperImage p cand.val =
        swapOracleImage p (bandedSparseAccessPaperImage p source.val) := by
    simpa [cand, candVal] using beq_iff_eq.mp hparts.1
  have himage :
      bandedSparseAccessPaperImage p pre.val =
        bandedSparseAccessPaperImage p cand.val := by
    rw [hpreImage, hcandImage]
  have hfin :
      pre = cand :=
    bandedSparseAccessPaperImage_injective_on_globalSlotSource
      p pre cand hn hkappa hκbits hpreSource hcandSource himage
  simpa [cand, candVal] using congrArg Fin.val hfin

/--
Proof-obligation interface for the active global-slot inverse-on-range route.

The record fixes the source predicate, image function, post-SWAP target, and
candidate preimage used by the corrected `O_D^BS` route.  The executable
`candidateChecks` field can be proved from
`bandedSparseAccessPaperGlobalSlotSource` by
`bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_globalSlotSource`.
The semantic inverse, uniqueness, injectivity, cleanup, and unitary-extension
fields remain false in Phase 1.
-/
structure BandedSparseAccessGlobalSlotInverseOnRangeContract where
  sourceAnchor : String
  sourcePredicate : String
  imageFunction : String
  preimageCandidate : String
  sourceIndex : Nat
  sourceRegisters : BandedSparseAccessPaperRegisters
  sourceInGlobalDomain : Bool
  postSwapImageIndex : Nat
  candidatePreimageIndex : Nat
  candidateChecks : Bool
  inverseOnRange : ObligationRecord
  uniquePreimage : ObligationRecord
  imageInjectiveOnGlobalSource : ObligationRecord
  daggerCleanup : ObligationRecord
  unitaryExtension : ObligationRecord
deriving Repr, DecidableEq

/--
Default global-source inverse-on-range contract for one `O_D^BS` source column.

This records the fixed route for future proof work without promoting any
semantic flag or changing the active forward/dagger matrices.
-/
def bandedSparseAccessGlobalSlotInverseOnRangeContract
    (p : OneTermRobinParameters) (source : Nat) :
    BandedSparseAccessGlobalSlotInverseOnRangeContract where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1 and Fig. 1-term Robin, arXiv:2506.20478"
  sourcePredicate := "bandedSparseAccessPaperGlobalSlotSource"
  imageFunction := "bandedSparseAccessPaperImage"
  preimageCandidate := "bandedSparseAccessPaperPostSwapPreimageCandidate"
  sourceIndex := source
  sourceRegisters := bandedSparseAccessPaperRegisters p source
  sourceInGlobalDomain := bandedSparseAccessPaperGlobalSlotSource p source
  postSwapImageIndex := swapOracleImage p (bandedSparseAccessPaperImage p source)
  candidatePreimageIndex :=
    bandedSparseAccessPaperPostSwapPreimageCandidate p source
  candidateChecks :=
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks p source
  inverseOnRange := {
    description := "the active global-slot preimage candidate maps by O_D^BS to the post-SWAP column on every global-source input"
    source := "QBE-AUTO-002 O_D^BS global-source inverse-on-range interface"
    proved := false
  }
  uniquePreimage := {
    description := "the active global-slot preimage candidate is the unique clean preimage of the post-SWAP column"
    source := "QBE-AUTO-002 O_D^BS global-source inverse-on-range interface"
    proved := false
  }
  imageInjectiveOnGlobalSource := {
    description := "bandedSparseAccessPaperImage is injective on the active global-slot clean source domain"
    source := "QBE-AUTO-002 O_D^BS global-source inverse-on-range interface"
    proved := false
  }
  daggerCleanup := {
    description := "(O_D^BS)^dagger cleans the active global-slot source image after SWAP"
    source := "Guseynov-Huang-Liu 2025, Fig. 1-term Robin and Lemma 1, arXiv:2506.20478"
    proved := false
  }
  unitaryExtension := {
    description := "the active global-slot image route extends to a full O_D^BS unitary"
    source := "Guseynov-Huang-Liu 2025, Lemma 1, arXiv:2506.20478"
    proved := false
  }

/-- The global-source inverse-on-range contract is obligation-only in Phase 1. -/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_flags_false
    (p : OneTermRobinParameters) (source : Nat) :
    (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).inverseOnRange.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).uniquePreimage.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).imageInjectiveOnGlobalSource.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).daggerCleanup.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).unitaryExtension.proved =
        false := by
  simp [bandedSparseAccessGlobalSlotInverseOnRangeContract]

/--
Global-source columns feed the fixed inverse-on-range interface and satisfy the
executable candidate audit.

The final fields remain false: this theorem does not assert uniqueness,
injectivity, semantic dagger cleanup, or unitarity.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
    (p : OneTermRobinParameters) (source : Nat)
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsourceFinite : source < qubitDim (oneTermRobinTotalQubits p))
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source = true) :
    (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).sourceInGlobalDomain =
        true ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).candidateChecks =
        true ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).inverseOnRange.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).uniquePreimage.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).imageInjectiveOnGlobalSource.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).daggerCleanup.proved =
        false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p source).unitaryExtension.proved =
        false := by
  have hchecks :
      bandedSparseAccessPaperPostSwapPreimageCandidateChecks p source = true :=
    bandedSparseAccessPaperPostSwapPreimageCandidateChecks_of_globalSlotSource
      p source hn hkappa hκbits hsourceFinite hsource
  simp [bandedSparseAccessGlobalSlotInverseOnRangeContract, hsource, hchecks]

/--
Record-level bridge from the compiled post-SWAP unique-preimage theorem to the
global-slot inverse-on-range contract.

This theorem reflects the finite basis-index evidence in the contract fields:
any active global-source preimage of the contract's post-SWAP target is the
contract's candidate preimage.  It deliberately keeps every semantic obligation
flag in the contract false; dagger cleanup and unitarity remain separate
Phase 1 obligations.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_uniquePreimageBridge
    (p : OneTermRobinParameters)
    (source pre : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true)
    (hpreSource : bandedSparseAccessPaperGlobalSlotSource p pre.val = true)
    (hpreImage :
      bandedSparseAccessPaperImage p pre.val =
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).postSwapImageIndex) :
    pre.val =
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidatePreimageIndex ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false := by
  have hpreImageTarget :
      bandedSparseAccessPaperImage p pre.val =
        swapOracleImage p (bandedSparseAccessPaperImage p source.val) := by
    simpa [bandedSparseAccessGlobalSlotInverseOnRangeContract] using hpreImage
  have hunique :
      pre.val =
        bandedSparseAccessPaperPostSwapPreimageCandidate p source.val :=
    bandedSparseAccessPaperPostSwapPreimageCandidate_unique_on_globalSlotSource
      p source pre hn hkappa hκbits hsource hpreSource hpreImageTarget
  have hcontract :
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false :=
    bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  exact ⟨by
    simpa [bandedSparseAccessGlobalSlotInverseOnRangeContract] using hunique,
    hcontract⟩

/--
Bridge the global-slot inverse-on-range contract to the concrete post-SWAP
dagger cleanup witness.

This theorem constructs the finite post-SWAP column and the named preimage
candidate from the active global-source route, then reuses
`BandedSparseAccessPostSwapCleanup` to expose the transpose-style dagger entry
and executable register checks.  It deliberately keeps the semantic
`daggerCleanup` and `unitaryExtension` flags false.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_daggerCleanupBridge
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    ∃ (post pre : Fin (qubitDim (oneTermRobinTotalQubits p))),
      BandedSparseAccessPostSwapCleanup p source post pre ∧
        post.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex ∧
        pre.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex ∧
        (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1 ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).unitaryExtension.proved = false := by
  let post : Fin (qubitDim (oneTermRobinTotalQubits p)) :=
    ⟨swapOracleImage p (bandedSparseAccessPaperImage p source.val), by
      have htwo : 2 ≤ p.n := by omega
      have haddrSource :
          bandedSparseAccessPaperAddress p source.val < (1 <<< p.n) := by
        have h := bandedSparseAccessPaperAddress_lt_gridSize_of_two_le
          p source.val htwo
        simpa [gridSize, Nat.one_shiftLeft] using h
      exact bandedSparseAccessPaperPostSwapImage_lt_qubitDim_of_address_lt
        p source haddrSource⟩
  let pre : Fin (qubitDim (oneTermRobinTotalQubits p)) :=
    ⟨bandedSparseAccessPaperPostSwapPreimageCandidate p source.val,
      bandedSparseAccessPaperPostSwapPreimageCandidate_lt_qubitDim_of_globalSlotSource
        p source hn hkappa hκbits hsource⟩
  have hcleanup :
      BandedSparseAccessPostSwapCleanup p source post pre := by
    simpa [post, pre] using
      bandedSparseAccessPostSwapCleanup_of_globalSlotSourceCandidate_noRange
        p source hn hkappa hκbits hsource
  have hcontract :
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false :=
    bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  refine ⟨post, pre, hcleanup, ?_, ?_, hcleanup.daggerEntry, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · exact hcontract.2.1
  · exact hcontract.2.2.2.2.2.1
  · exact hcontract.2.2.2.2.2.2

/--
Reviewed cleanup-contract map for the active global-slot `O_D^BS` route.

This wrapper is intentionally non-promoting.  It combines the compiled
post-SWAP cleanup witness with the record-level unique-preimage bridge, so
later cleanup work can consume one theorem exposing the contract target,
candidate preimage, active-source uniqueness, and transpose-style dagger entry.
The semantic inverse, uniqueness, injectivity, cleanup, and unitary-extension
obligation flags remain false.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_cleanupContractMap
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    ∃ (post pre : Fin (qubitDim (oneTermRobinTotalQubits p))),
      BandedSparseAccessPostSwapCleanup p source post pre ∧
        post.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex ∧
        pre.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex ∧
        bandedSparseAccessPaperGlobalSlotSource p pre.val = true ∧
        (∀ (pre' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          bandedSparseAccessPaperGlobalSlotSource p pre'.val = true →
          bandedSparseAccessPaperImage p pre'.val = post.val →
          pre'.val = pre.val) ∧
        (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1 ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).unitaryExtension.proved = false := by
  rcases bandedSparseAccessGlobalSlotInverseOnRangeContract_daggerCleanupBridge
      p source hn hkappa hκbits hsource with
    ⟨post, pre, hcleanup, hpost, hpre, hentry, hchecks, hdaggerFlag,
      hunitaryFlag⟩
  have hcontract :
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false :=
    bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  have hpreGlobalCandidate :
      bandedSparseAccessPaperGlobalSlotSource p
        (bandedSparseAccessPaperPostSwapPreimageCandidate p source.val) = true :=
    bandedSparseAccessPaperPostSwapPreimageCandidate_globalSlotSource_of_globalSlotSource
      p source hn hkappa hκbits hsource
  have hpreSource :
      bandedSparseAccessPaperGlobalSlotSource p pre.val = true := by
    rw [hpre]
    simpa [bandedSparseAccessGlobalSlotInverseOnRangeContract]
      using hpreGlobalCandidate
  have hunique :
      ∀ (pre' : Fin (qubitDim (oneTermRobinTotalQubits p))),
        bandedSparseAccessPaperGlobalSlotSource p pre'.val = true →
        bandedSparseAccessPaperImage p pre'.val = post.val →
        pre'.val = pre.val := by
    intro pre' hpreSource' hpreImage'
    have hpreImageContract :
        bandedSparseAccessPaperImage p pre'.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex :=
      hpreImage'.trans hpost
    have hbridge :=
      bandedSparseAccessGlobalSlotInverseOnRangeContract_uniquePreimageBridge
        p source pre' hn hkappa hκbits hsource hpreSource'
        hpreImageContract
    exact hbridge.1.trans hpre.symm
  refine ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hunique, hentry,
    hchecks, ?_, ?_, ?_, hdaggerFlag, hunitaryFlag⟩
  · exact hcontract.2.2.1
  · exact hcontract.2.2.2.1
  · exact hcontract.2.2.2.2.1

/--
Default-paper-contract cleanup-route bridge for the active global-slot
`O_D^BS` route.

This theorem ties the compiled cleanup-contract map back to
`defaultBandedSparseAccessPaperContract p`.  It exposes the post-SWAP cleanup
witness, active-source uniqueness, and transpose-style dagger entry while
recording that the paper-contract cleanup and unitary-extension flags, and the
two active `O_D^BS` gate-unitarity flags, remain false.
-/
theorem defaultBandedSparseAccessPaperContract_cleanupRouteBridge
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    ∃ (post pre : Fin (qubitDim (oneTermRobinTotalQubits p))),
      BandedSparseAccessPostSwapCleanup p source post pre ∧
        post.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex ∧
        pre.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex ∧
        bandedSparseAccessPaperGlobalSlotSource p pre.val = true ∧
        (∀ (pre' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          bandedSparseAccessPaperGlobalSlotSource p pre'.val = true →
          bandedSparseAccessPaperImage p pre'.val = post.val →
          pre'.val = pre.val) ∧
        (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1 ∧
        (defaultBandedSparseAccessPaperContract p).daggerCleanup.proved =
          false ∧
        (defaultBandedSparseAccessPaperContract p).unitaryExtension.proved =
          false ∧
        (oneTermRobinGate_O_D_BS p).unitary.proved = false ∧
        (oneTermRobinGate_O_D_BS_dagger p).unitary.proved = false := by
  rcases bandedSparseAccessGlobalSlotInverseOnRangeContract_cleanupContractMap
      p source hn hkappa hκbits hsource with
    ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hunique, hentry,
      _hchecks, _hinverseFlag, _huniqueFlag, _himageFlag, _hdaggerFlag,
      _hunitaryFlag⟩
  refine ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hunique, hentry,
    ?_, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · rfl
  · rfl

/--
Off-candidate dagger entries are zero on the active global-slot source domain.

For the fixed post-SWAP target in the global-slot inverse-on-range contract,
any other active global-source preimage whose index is not the named candidate
cannot have a transpose-style `(O_D^BS)^†` entry into that target.  This is a
matrix-entry bridge only: it does not promote dagger cleanup or unitary flags.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_daggerOffCandidate_zero
    (p : OneTermRobinParameters)
    (source other post : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true)
    (hotherSource : bandedSparseAccessPaperGlobalSlotSource p other.val = true)
    (hpost :
      post.val =
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).postSwapImageIndex)
    (hne :
      other.val ≠
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidatePreimageIndex) :
    (oneTermRobinGate_O_D_BS_dagger p).matrix other post = Coeff.rat 0 ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false := by
  have hnotImage :
      ¬ post.val = bandedSparseAccessPaperImage p other.val := by
    intro himage
    have hotherImage :
        bandedSparseAccessPaperImage p other.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex :=
      himage.symm.trans hpost
    have hbridge :=
      bandedSparseAccessGlobalSlotInverseOnRangeContract_uniquePreimageBridge
        p source other hn hkappa hκbits hsource hotherSource hotherImage
    exact hne hbridge.1
  have hentry :
      (oneTermRobinGate_O_D_BS_dagger p).matrix other post = Coeff.rat 0 := by
    simp [oneTermRobinGate_O_D_BS_dagger,
      bandedSparseAccessPaperDaggerMatrix, hnotImage]
  have hcontract :
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false :=
    bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  exact ⟨hentry, hcontract.2.2.2.2.2.1, hcontract.2.2.2.2.2.2⟩

/--
Restricted active-domain dagger-column cleanup for the global-slot route.

For the contract post-SWAP target, the named candidate has dagger entry `1`,
and every other active global-source row has dagger entry `0`.  This is only a
column statement over `bandedSparseAccessPaperGlobalSlotSource`; it does not
promote semantic cleanup, unitarity, circuit-unitarity, or block-extraction
obligations.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_restrictedDaggerColumnCleanup
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    ∃ (post pre : Fin (qubitDim (oneTermRobinTotalQubits p))),
      BandedSparseAccessPostSwapCleanup p source post pre ∧
        post.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex ∧
        pre.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex ∧
        bandedSparseAccessPaperGlobalSlotSource p pre.val = true ∧
        (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1 ∧
        (∀ (other : Fin (qubitDim (oneTermRobinTotalQubits p))),
          bandedSparseAccessPaperGlobalSlotSource p other.val = true →
          other.val ≠ pre.val →
          (oneTermRobinGate_O_D_BS_dagger p).matrix other post =
            Coeff.rat 0) ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).unitaryExtension.proved = false ∧
        (defaultBandedSparseAccessPaperContract p).daggerCleanup.proved =
          false ∧
        (defaultBandedSparseAccessPaperContract p).unitaryExtension.proved =
          false ∧
        (oneTermRobinGate_O_D_BS p).unitary.proved = false ∧
        (oneTermRobinGate_O_D_BS_dagger p).unitary.proved = false ∧
        (defaultOneTermRobinTheoremData p).obligations.circuitUnitary.proved =
          false ∧
        (defaultOneTermRobinTheoremData p).obligations.blockExtraction.proved =
          false := by
  rcases defaultBandedSparseAccessPaperContract_cleanupRouteBridge
      p source hn hkappa hκbits hsource with
    ⟨post, pre, hcleanup, hpost, hpre, hpreSource, _hunique, hentry,
      hpaperCleanupFlag, hpaperUnitaryFlag, hforwardUnitaryFlag,
      hdaggerUnitaryFlag⟩
  have hcontract :
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false :=
    bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  have hzero :
      ∀ (other : Fin (qubitDim (oneTermRobinTotalQubits p))),
        bandedSparseAccessPaperGlobalSlotSource p other.val = true →
        other.val ≠ pre.val →
        (oneTermRobinGate_O_D_BS_dagger p).matrix other post =
          Coeff.rat 0 := by
    intro other hotherSource hotherNePre
    have hotherNeContract :
        other.val ≠
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex := by
      intro hotherEqContract
      exact hotherNePre (hotherEqContract.trans hpre.symm)
    exact
      (bandedSparseAccessGlobalSlotInverseOnRangeContract_daggerOffCandidate_zero
        p source other post hn hkappa hκbits hsource hotherSource hpost
        hotherNeContract).1
  refine ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hentry, hzero,
    ?_, ?_, hpaperCleanupFlag, hpaperUnitaryFlag, hforwardUnitaryFlag,
    hdaggerUnitaryFlag, ?_, ?_⟩
  · exact hcontract.2.2.2.2.2.1
  · exact hcontract.2.2.2.2.2.2
  · rfl
  · rfl

/--
Indicator form of the restricted active-domain dagger column.

This is the same active-source-only column statement as
`bandedSparseAccessGlobalSlotInverseOnRangeContract_restrictedDaggerColumnCleanup`,
rewritten as one if-then-else formula.  It does not promote inverse,
cleanup, unitarity, circuit-unitarity, or block-extraction obligations.
-/
theorem bandedSparseAccessGlobalSlotInverseOnRangeContract_restrictedDaggerColumnIndicator
    (p : OneTermRobinParameters)
    (source : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (hn : 3 <= p.n) (hkappa : p.kappa = 7) (hκbits : clog2 p.kappa = 3)
    (hsource : bandedSparseAccessPaperGlobalSlotSource p source.val = true) :
    ∃ (post pre : Fin (qubitDim (oneTermRobinTotalQubits p))),
      BandedSparseAccessPostSwapCleanup p source post pre ∧
        post.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex ∧
        pre.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex ∧
        bandedSparseAccessPaperGlobalSlotSource p pre.val = true ∧
        (∀ (other : Fin (qubitDim (oneTermRobinTotalQubits p))),
          bandedSparseAccessPaperGlobalSlotSource p other.val = true →
          (oneTermRobinGate_O_D_BS_dagger p).matrix other post =
            if other.val = pre.val then Coeff.rat 1 else Coeff.rat 0) ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).unitaryExtension.proved = false ∧
        (defaultBandedSparseAccessPaperContract p).daggerCleanup.proved =
          false ∧
        (defaultBandedSparseAccessPaperContract p).unitaryExtension.proved =
          false ∧
        (oneTermRobinGate_O_D_BS p).unitary.proved = false ∧
        (oneTermRobinGate_O_D_BS_dagger p).unitary.proved = false ∧
        (defaultOneTermRobinTheoremData p).obligations.circuitUnitary.proved =
          false ∧
        (defaultOneTermRobinTheoremData p).obligations.blockExtraction.proved =
          false := by
  rcases bandedSparseAccessGlobalSlotInverseOnRangeContract_restrictedDaggerColumnCleanup
      p source hn hkappa hκbits hsource with
    ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hentry, hzero,
      hcontractCleanupFlag, hcontractUnitaryFlag, hpaperCleanupFlag,
      hpaperUnitaryFlag, hforwardUnitaryFlag, hdaggerUnitaryFlag,
      htheoremCircuitFlag, htheoremBlockFlag⟩
  have hcontract :
      (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).sourceInGlobalDomain = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).candidateChecks = true ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).inverseOnRange.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).uniquePreimage.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).imageInjectiveOnGlobalSource.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).daggerCleanup.proved = false ∧
        (bandedSparseAccessGlobalSlotInverseOnRangeContract p
          source.val).unitaryExtension.proved = false :=
    bandedSparseAccessGlobalSlotInverseOnRangeContract_of_globalSlotSource
      p source.val hn hkappa hκbits source.2 hsource
  have hindicator :
      ∀ (other : Fin (qubitDim (oneTermRobinTotalQubits p))),
        bandedSparseAccessPaperGlobalSlotSource p other.val = true →
        (oneTermRobinGate_O_D_BS_dagger p).matrix other post =
          if other.val = pre.val then Coeff.rat 1 else Coeff.rat 0 := by
    intro other hotherSource
    by_cases hotherPre : other.val = pre.val
    · have hotherEq : other = pre := Fin.ext hotherPre
      subst other
      simp [hentry]
    · exact (by
        simp [hotherPre, hzero other hotherSource hotherPre])
  refine ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hindicator,
    ?_, ?_, ?_, hcontractCleanupFlag, hcontractUnitaryFlag, hpaperCleanupFlag,
    hpaperUnitaryFlag, hforwardUnitaryFlag, hdaggerUnitaryFlag,
    htheoremCircuitFlag, htheoremBlockFlag⟩
  · exact hcontract.2.2.1
  · exact hcontract.2.2.2.1
  · exact hcontract.2.2.2.2.1

/--
Allowed scopes for the next `O_D^BS` cleanup theorem packet.

This is planning data for Phase 1 faithful-paper work.  Selecting a scope here
does not prove cleanup, full-domain injectivity, or unitary extension.
-/
inductive BandedSparseAccessCleanupScope where
  | activeGlobalSource
  | fullCleanDomain
  | fullSpace
deriving Repr, DecidableEq

/--
Non-promoting decision for the next `O_D^BS` cleanup theorem domain.

The current compiled matrix-entry theorem is restricted to active global-source
rows.  Full clean-domain cleanup still needs a reversible image rule for every
clean unused sparse branch, and full-space cleanup/unitarity still needs a
separate reversible-extension argument.  This record keeps that boundary
machine-checkable before any lower proof packet tries to promote
`daggerCleanup`.
-/
structure BandedSparseAccessCleanupScopeDecision where
  sourceAnchor : String
  selectedScope : BandedSparseAccessCleanupScope
  selectedPredicate : String
  selectedEvidence : String
  fullCleanDomainSelected : Bool
  fullSpaceSelected : Bool
  semanticCleanupPromotionAllowed : Bool
  paperContractCleanup : ObligationRecord
  fullCleanDomainCleanup : ObligationRecord
  fullSpaceUnitaryExtension : ObligationRecord
deriving Repr, DecidableEq

/--
Default cleanup-scope decision after the restricted dagger-column indicator.

The selected theorem domain is active global-source only.  The surrounding
obligation records are copied from the existing paper and full-domain contracts
so their `proved = false` status stays synchronized with the actual contracts.
-/
def bandedSparseAccessCleanupScopeDecision
    (p : OneTermRobinParameters) :
    BandedSparseAccessCleanupScopeDecision where
  sourceAnchor := "Guseynov-Huang-Liu 2025, Lemma 1 and Fig. 1-term Robin, arXiv:2506.20478"
  selectedScope := BandedSparseAccessCleanupScope.activeGlobalSource
  selectedPredicate := "bandedSparseAccessPaperGlobalSlotSource"
  selectedEvidence :=
    "bandedSparseAccessGlobalSlotInverseOnRangeContract_restrictedDaggerColumnIndicator"
  fullCleanDomainSelected := false
  fullSpaceSelected := false
  semanticCleanupPromotionAllowed := false
  paperContractCleanup := (defaultBandedSparseAccessPaperContract p).daggerCleanup
  fullCleanDomainCleanup :=
    (bandedSparseAccessFullCleanDomainExtensionContract p).daggerCleanup
  fullSpaceUnitaryExtension :=
    (defaultBandedSparseAccessPaperContract p).unitaryExtension

/--
The cleanup-scope decision selects the active global-source theorem and keeps
all broader cleanup/unitarity obligations closed to proof-flag promotion.
-/
theorem bandedSparseAccessCleanupScopeDecision_activeGlobalSource
    (p : OneTermRobinParameters) :
    (bandedSparseAccessCleanupScopeDecision p).selectedScope =
        BandedSparseAccessCleanupScope.activeGlobalSource ∧
      (bandedSparseAccessCleanupScopeDecision p).selectedPredicate =
        "bandedSparseAccessPaperGlobalSlotSource" ∧
      (bandedSparseAccessCleanupScopeDecision p).selectedEvidence =
        "bandedSparseAccessGlobalSlotInverseOnRangeContract_restrictedDaggerColumnIndicator" ∧
      (bandedSparseAccessCleanupScopeDecision p).fullCleanDomainSelected =
        false ∧
      (bandedSparseAccessCleanupScopeDecision p).fullSpaceSelected = false ∧
      (bandedSparseAccessCleanupScopeDecision p).semanticCleanupPromotionAllowed =
        false ∧
      (bandedSparseAccessCleanupScopeDecision p).paperContractCleanup.proved =
        false ∧
      (bandedSparseAccessCleanupScopeDecision p).fullCleanDomainCleanup.proved =
        false ∧
      (bandedSparseAccessCleanupScopeDecision p).fullSpaceUnitaryExtension.proved =
        false := by
  simp [bandedSparseAccessCleanupScopeDecision,
    defaultBandedSparseAccessPaperContract,
    bandedSparseAccessFullCleanDomainExtensionContract]

/--
The cleanup-scope decision does not accept the prior PDE sparse-access
transcript as a full-space unitary-extension proof.

This is a guard for the next Phase 1 source-contract packet: the prior paper's
equation is recorded as a source anchor, while its resource proof and any
Robin-specific reversible-extension use remain unproved in QBE.
-/
theorem bandedSparseAccessCleanupScopeDecision_priorPDESourceTranscriptGuard
    (p : OneTermRobinParameters) :
    (bandedSparseAccessCleanupScopeDecision p).selectedScope =
        BandedSparseAccessCleanupScope.activeGlobalSource ∧
      (bandedSparseAccessCleanupScopeDecision p).fullSpaceSelected = false ∧
      (bandedSparseAccessCleanupScopeDecision p).fullSpaceUnitaryExtension.proved =
        false ∧
      bandedSparseAccessPriorPDESourceContract.oracleEquation =
        "O_A^BS |0>^(n-l)|s>^l|i>^n = |r_si>^n|i>^n" ∧
      bandedSparseAccessPriorPDESourceContract.resourceClaim.proved = false ∧
      bandedSparseAccessPriorPDESourceContract.robinUnusedBranchImageRule =
        none ∧
      bandedSparseAccessPriorPDESourceContract.closesUnusedZeroBranchExtension =
        false ∧
      bandedSparseAccessPriorPDESourceContract.lowerProofSearchAllowed =
        false ∧
      (defaultBandedSparseAccessPaperContract p).unitaryExtension.proved =
        false := by
  simp [bandedSparseAccessCleanupScopeDecision,
    defaultBandedSparseAccessPaperContract,
    bandedSparseAccessPriorPDESourceContract]

/--
The cleanup-scope decision keeps the full clean-domain image-rule slot blocked.

This guard ties the active-global-source scope choice to the unused-branch
source decision and the full clean-domain wrapper.  It is not a cleanup or
unitarity theorem: the missing image rule remains `none`, proof search remains
disabled, and every full clean-domain semantic field stays false.
-/
theorem bandedSparseAccessCleanupScopeDecision_fullCleanDomainImageRuleBlocked
    (p : OneTermRobinParameters) (j : Nat) :
    (bandedSparseAccessCleanupScopeDecision p).selectedScope =
        BandedSparseAccessCleanupScope.activeGlobalSource ∧
      (bandedSparseAccessCleanupScopeDecision p).fullCleanDomainSelected =
        false ∧
      (bandedSparseAccessCleanupScopeDecision p).semanticCleanupPromotionAllowed =
        false ∧
      (bandedSparseAccessCleanupScopeDecision p).fullCleanDomainCleanup.proved =
        false ∧
      bandedSparseAccessUnusedZeroBranchSourceDecision.lowerProofSearchAllowed =
        false ∧
      (bandedSparseAccessUnusedBranchImageRuleContract p j).proposedImageIndex =
        none ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract
        j).proposedImageIndex = none ∧
      ((bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageRuleContract
        j).imageSpecified.proved = false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unusedBranchImageSpecified.proved =
        false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).fullCleanDomainInjective.proved =
        false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).daggerCleanup.proved =
        false ∧
      (bandedSparseAccessFullCleanDomainExtensionContract p).unitaryExtension.proved =
        false := by
  simp [bandedSparseAccessCleanupScopeDecision,
    bandedSparseAccessUnusedZeroBranchSourceDecision,
    bandedSparseAccessUnusedBranchImageRuleContract,
    bandedSparseAccessFullCleanDomainExtensionContract]

/--
Concrete boundary-source regression for the default paper-contract cleanup route.

The historical source column `48` is outside the rejected row-dependent valid
source predicate, but it is an active global-slot source for Lemma 1.  This
instance routes that column through the default cleanup bridge without
promoting any `O_D^BS` semantic proof flag.
-/
theorem defaultBandedSparseAccessPaperContract_cleanupRouteBridge_boundaryColumn_n3 :
    let p : OneTermRobinParameters :=
      { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
    let source : Fin (qubitDim (oneTermRobinTotalQubits p)) :=
      ⟨48, by native_decide⟩
    ∃ (post pre : Fin (qubitDim (oneTermRobinTotalQubits p))),
      BandedSparseAccessPostSwapCleanup p source post pre ∧
        post.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).postSwapImageIndex ∧
        pre.val =
          (bandedSparseAccessGlobalSlotInverseOnRangeContract p
            source.val).candidatePreimageIndex ∧
        bandedSparseAccessPaperGlobalSlotSource p source.val = true ∧
        bandedSparseAccessPaperValidCleanSource p source.val = false ∧
        bandedSparseAccessPaperGlobalSlotSource p pre.val = true ∧
        (∀ (pre' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          bandedSparseAccessPaperGlobalSlotSource p pre'.val = true →
          bandedSparseAccessPaperImage p pre'.val = post.val →
          pre'.val = pre.val) ∧
        (oneTermRobinGate_O_D_BS_dagger p).matrix pre post = Coeff.rat 1 ∧
        (defaultBandedSparseAccessPaperContract p).daggerCleanup.proved =
          false ∧
        (defaultBandedSparseAccessPaperContract p).unitaryExtension.proved =
          false ∧
        (oneTermRobinGate_O_D_BS p).unitary.proved = false ∧
        (oneTermRobinGate_O_D_BS_dagger p).unitary.proved = false := by
  let p : OneTermRobinParameters :=
    { n := 3, kappa := 7, functionPieces := 1, polynomialDegreeCost := 1 }
  let source : Fin (qubitDim (oneTermRobinTotalQubits p)) :=
    ⟨48, by native_decide⟩
  have hsource :
      bandedSparseAccessPaperGlobalSlotSource p source.val = true := by
    native_decide
  have hvalidSourceRejected :
      bandedSparseAccessPaperValidCleanSource p source.val = false := by
    native_decide
  rcases defaultBandedSparseAccessPaperContract_cleanupRouteBridge
      p source (by native_decide) rfl (by native_decide) hsource with
    ⟨post, pre, hcleanup, hpost, hpre, hpreSource, hunique, hentry,
      hpaperCleanupFlag, hpaperUnitaryFlag, hforwardUnitaryFlag,
      hdaggerUnitaryFlag⟩
  exact ⟨post, pre, hcleanup, hpost, hpre, hsource, hvalidSourceRejected,
    hpreSource, hunique, hentry, hpaperCleanupFlag, hpaperUnitaryFlag,
    hforwardUnitaryFlag, hdaggerUnitaryFlag⟩

/--
Cycle 12: robinIndicatorBitPosition = 1 + 2*p.n, hence >= 1 + p.n.
-/
theorem robinIndicatorBitPosition_ge (p : OneTermRobinParameters) :
    robinIndicatorBitPosition p ≥ 1 + p.n := by
  unfold robinIndicatorBitPosition defaultRobinRegisterPartition
  simp only
  omega

/--
Cycle 12: The system register value is preserved by indicatorOracleImage.
XORing with a bit at position indPos = 1 + 2n does not affect bits [1, 1+n).
main.tex:1088-1099 --/
theorem indicatorOracleImage_systemVal_preserved (p : OneTermRobinParameters) (j : Nat) :
    ((indicatorOracleImage p j) >>> 1) &&& ((1 <<< p.n) - 1) =
    (j >>> 1) &&& ((1 <<< p.n) - 1) := by
  show (j ^^^ (if (2 : Nat) ≤ (j >>> 1) &&& (1 <<< p.n - 1) ∧
      (j >>> 1) &&& (1 <<< p.n - 1) ≤ gridSize p.n - 3 then 1 else 0) <<<
      robinIndicatorBitPosition p) >>> 1 &&& (1 <<< p.n - 1) =
    j >>> 1 &&& (1 <<< p.n - 1)
  apply xor_shift_preserve_shift_low
  exact robinIndicatorBitPosition_ge p

/--
Cycle 12: The isBulk predicate gives the same result for j and indicatorOracleImage p j,
because isBulk only depends on the system register value, which is preserved.
main.tex:1088-1099 --/
theorem indicatorOracleImage_isBulk_preserved (p : OneTermRobinParameters) (j : Nat) :
    (if (2 : Nat) ≤ ((indicatorOracleImage p j) >>> 1) &&& ((1 <<< p.n) - 1) ∧
        ((indicatorOracleImage p j) >>> 1) &&& ((1 <<< p.n) - 1) ≤ gridSize p.n - 3
     then (1 : Nat) else 0) =
    (if (2 : Nat) ≤ (j >>> 1) &&& ((1 <<< p.n) - 1) ∧
        (j >>> 1) &&& ((1 <<< p.n) - 1) ≤ gridSize p.n - 3
     then (1 : Nat) else 0) := by
  have h := indicatorOracleImage_systemVal_preserved p j
  split <;> split <;> simp_all

/--
Cycle 12: General self-inverse property for indicatorOracleImage.
Applying the indicator oracle image twice returns the original value for all j,
because the indicator bit is XORed twice (and isBulk is preserved).
main.tex:1088-1099 --/
theorem indicatorOracleImage_self_inverse (p : OneTermRobinParameters) (j : Nat) :
    indicatorOracleImage p (indicatorOracleImage p j) = j := by
  simp only [indicatorOracleImage]
  have h_pres := indicatorOracleImage_isBulk_preserved p j
  simp only [indicatorOracleImage] at h_pres
  rw [h_pres]
  rw [Nat.xor_assoc, Nat.xor_self, Nat.xor_zero]

/--
Source-facing bridge for the explicit `U_indic^dagger` transcript slot.

The dagger slot uses the same matrix as `U_indic` because the underlying
indicator image is self-inverse.  This theorem records the bridge used by the
conversion window; it does not change the active backend gate list.
-/
theorem oneTermRobinGate_U_indic_dagger_selfInverseBridge
    (p : OneTermRobinParameters) :
    (oneTermRobinGate_U_indic_dagger p).matrix =
        (oneTermRobinGate_U_indic p).matrix ∧
      (∀ j : Nat, indicatorOracleImage p (indicatorOracleImage p j) = j) := by
  exact ⟨oneTermRobinGate_U_indic_dagger_matrix_eq p,
    indicatorOracleImage_self_inverse p⟩

/--
Cycle 12: General injectivity for indicatorOracleImage, derived from self-inverse.
main.tex:1088-1099 --/
theorem indicatorOracleImage_injective (p : OneTermRobinParameters) {j₁ j₂ : Nat}
    (h : indicatorOracleImage p j₁ = indicatorOracleImage p j₂) :
    j₁ = j₂ := by
  have h1 := indicatorOracleImage_self_inverse p j₁
  have h2 := indicatorOracleImage_self_inverse p j₂
  rw [← h1, ← h2, h]

/--
Cycle 12: robinIndicatorBitPosition is strictly below oneTermRobinTotalQubits.
indPos = 1 + 2n < 2n + clog2 n + clog2 fp + 5 = totalQubits, since clog2 ≥ 0 and 5 > 1.
-/
theorem robinIndicatorBitPosition_lt_totalQubits (p : OneTermRobinParameters) :
    robinIndicatorBitPosition p < oneTermRobinTotalQubits p := by
  simp only [robinIndicatorBitPosition, oneTermRobinTotalQubits,
    RobinRegisterPartition.totalQubits, defaultRobinRegisterPartition]
  omega

/--
Cycle 12: indicatorOracleImage preserves the qubitDim bound.
When j < 2^totalQubits, the image is also < 2^totalQubits, because the XOR
operand is either 0 or a single bit at position indPos < totalQubits.
-/
theorem indicatorOracleImage_lt (p : OneTermRobinParameters) {j : Nat}
    (hj : j < qubitDim (oneTermRobinTotalQubits p)) :
    indicatorOracleImage p j < qubitDim (oneTermRobinTotalQubits p) := by
  simp only [qubitDim, gridSize] at *
  show j ^^^ (if (2 : Nat) ≤ (j >>> 1) &&& (1 <<< p.n - 1) ∧
      (j >>> 1) &&& (1 <<< p.n - 1) ≤ gridSize p.n - 3 then 1 else 0) <<<
      robinIndicatorBitPosition p < 2 ^ oneTermRobinTotalQubits p
  split
  · apply Nat.xor_lt_two_pow hj
    rw [Nat.one_shiftLeft]
    exact Nat.pow_lt_pow_of_lt (by omega) (robinIndicatorBitPosition_lt_totalQubits p)
  · simp only [Nat.zero_shiftLeft, Nat.xor_zero]; exact hj

/--
Cycle 12: Bijectivity of indicatorOracleImage on the Fin domain.
A self-inverse function on a finite type is bijective:
injective by cancellation, surjective because image(image(j)) = j.
main.tex:1088-1099 --/
theorem indicatorOracleImage_bijective (p : OneTermRobinParameters) :
    (∀ (a b : Fin (qubitDim (oneTermRobinTotalQubits p))),
        (⟨indicatorOracleImage p a.val, indicatorOracleImage_lt p a.2⟩ :
          Fin (qubitDim (oneTermRobinTotalQubits p))) =
        ⟨indicatorOracleImage p b.val, indicatorOracleImage_lt p b.2⟩ →
        a = b) ∧
    ∀ (y : Fin (qubitDim (oneTermRobinTotalQubits p))),
      ∃ (x : Fin (qubitDim (oneTermRobinTotalQubits p))),
        (⟨indicatorOracleImage p x.val, indicatorOracleImage_lt p x.2⟩ :
          Fin (qubitDim (oneTermRobinTotalQubits p))) = y := by
  constructor
  · intro a b h
    apply Fin.ext
    exact indicatorOracleImage_injective p (Fin.ext_iff.mp h)
  · intro y
    refine ⟨⟨indicatorOracleImage p y.val, indicatorOracleImage_lt p y.2⟩, ?_⟩
    apply Fin.ext
    exact indicatorOracleImage_self_inverse p y.val

/--
Cycle 12: For each column j, there is exactly one row i with M[i][j] = 1,
namely i = ⟨indicatorOracleImage p j.val, ...⟩.
main.tex:1088-1099 --/
theorem indicatorOracleMatrix_col_has_one (p : OneTermRobinParameters)
    (j : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    indicatorOracleMatrix p
      (⟨indicatorOracleImage p j.val, indicatorOracleImage_lt p j.2⟩ :
        Fin (qubitDim (oneTermRobinTotalQubits p))) j = Coeff.rat 1 := by
  rw [indicatorOracleMatrix_eq_image]
  simp

/--
Cycle 12: For each column j, any row i with M[i][j] = 1 must equal
⟨indicatorOracleImage p j.val, ...⟩, so the 1-entry is unique per column.
main.tex:1088-1099 --/
theorem indicatorOracleMatrix_col_unique (p : OneTermRobinParameters)
    (i j : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (h : indicatorOracleMatrix p i j = Coeff.rat 1) :
    i = ⟨indicatorOracleImage p j.val, indicatorOracleImage_lt p j.2⟩ := by
  rw [indicatorOracleMatrix_eq_image] at h
  split at h
  · next h_cond => exact Fin.ext h_cond
  · next h_cond => simp at h

/--
Cycle 12: For each row i, there exists a column j with M[i][j] = 1,
from surjectivity of indicatorOracleImage.
main.tex:1088-1099 --/
theorem indicatorOracleMatrix_row_has_one (p : OneTermRobinParameters)
    (i : Fin (qubitDim (oneTermRobinTotalQubits p))) :
    ∃ (j : Fin (qubitDim (oneTermRobinTotalQubits p))),
      indicatorOracleMatrix p i j = Coeff.rat 1 := by
  have h_surj := (indicatorOracleImage_bijective p).2 i
  have ⟨⟨xval, xprop⟩, hx⟩ := h_surj
  refine ⟨⟨xval, xprop⟩, ?_⟩
  rw [indicatorOracleMatrix_eq_image]
  have h_eq : i.val = indicatorOracleImage p xval := by
    have := Fin.ext_iff.mp hx
    simp at this
    exact this.symm
  simp [h_eq]

/--
Cycle 12: For each row i, the column j with M[i][j] = 1 is unique,
from injectivity of indicatorOracleImage.
main.tex:1088-1099 --/
theorem indicatorOracleMatrix_row_unique (p : OneTermRobinParameters)
    (i : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (j₁ j₂ : Fin (qubitDim (oneTermRobinTotalQubits p)))
    (h₁ : indicatorOracleMatrix p i j₁ = Coeff.rat 1)
    (h₂ : indicatorOracleMatrix p i j₂ = Coeff.rat 1) :
    j₁ = j₂ := by
  have key₁ := indicatorOracleMatrix_col_unique p i j₁ h₁
  have key₂ := indicatorOracleMatrix_col_unique p i j₂ h₂
  have h_inj := (indicatorOracleImage_bijective p).1
  exact h_inj j₁ j₂ (key₁.symm.trans key₂)

/--
Cycle 12: indicatorOracleMatrix is a permutation matrix: each row has exactly
one entry equal to 1, and each column has exactly one entry equal to 1.
This follows from indicatorOracleImage being a bijection on the Fin domain.
main.tex:1088-1099 --/
theorem indicatorOracleMatrix_is_permutation (p : OneTermRobinParameters) :
    (∀ (i : Fin (qubitDim (oneTermRobinTotalQubits p))),
      ∃ (j : Fin (qubitDim (oneTermRobinTotalQubits p))),
        indicatorOracleMatrix p i j = Coeff.rat 1 ∧
        ∀ (j' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          indicatorOracleMatrix p i j' = Coeff.rat 1 → j' = j) ∧
    (∀ (j : Fin (qubitDim (oneTermRobinTotalQubits p))),
      ∃ (i : Fin (qubitDim (oneTermRobinTotalQubits p))),
        indicatorOracleMatrix p i j = Coeff.rat 1 ∧
        ∀ (i' : Fin (qubitDim (oneTermRobinTotalQubits p))),
          indicatorOracleMatrix p i' j = Coeff.rat 1 → i' = i) := by
  constructor
  · intro i
    have ⟨j, hj⟩ := indicatorOracleMatrix_row_has_one p i
    exact ⟨j, hj, fun j' hj' => (indicatorOracleMatrix_row_unique p i j j' hj hj').symm⟩
  · intro j
    let row := (⟨indicatorOracleImage p j.val, indicatorOracleImage_lt p j.2⟩ :
                  Fin (qubitDim (oneTermRobinTotalQubits p)))
    exact ⟨row, indicatorOracleMatrix_col_has_one p j,
           fun i' hi' => indicatorOracleMatrix_col_unique p i' j hi'⟩

end GHL2025
end QuantumBlockEncoding
