$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskPriorLeanPath = $env:LEAN_PATH
Push-Location -LiteralPath $taskRepoRoot
try {
  New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache/QuantumBlockEncoding" | Out-Null
  $env:LEAN_PATH = "$PSScriptRoot/.cache"
  $taskSources = @(
    @('QuantumBlockEncoding/HermitePolynomial.lean','QuantumBlockEncoding/HermitePolynomial'),
    @('QuantumBlockEncoding/HermiteStatePreparation.lean','QuantumBlockEncoding/HermiteStatePreparation'),
    @('QuantumBlockEncoding/HermiteIntervalMass.lean','QuantumBlockEncoding/HermiteIntervalMass'),
    @('experiments/hermite-polynomial/precision/coefficient-range/CoefficientRange.lean','CoefficientRange'),
    @('experiments/hermite-polynomial/precision/finite-exp/FiniteExp.lean','FiniteExp'),
    @('experiments/hermite-polynomial/precision/finite-exp-degree/FiniteExpDegree.lean','FiniteExpDegree'),
    @('experiments/hermite-polynomial/precision/finite-middle-source/FiniteMiddleSource.lean','FiniteMiddleSource'),
    @('experiments/hermite-polynomial/precision/finite-middle-source/ConsumerChecks.lean','ConsumerChecks'),
    @('experiments/hermite-polynomial/precision/NormalizationStability.lean','NormalizationStability'),
    @('experiments/hermite-polynomial/precision/radius-supplier/RadiusSupplier.lean','RadiusSupplier'),
    @('experiments/hermite-polynomial/precision/radius-stability/RadiusStability.lean','RadiusStability'),
    @('experiments/hermite-polynomial/precision/global-radius-budget/GlobalRadiusBudget.lean','GlobalRadiusBudget'),
    @('experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseSourceBudget.lean','PiecewiseSourceBudget'),
    @('QuantumBlockEncoding/HermiteTransferCores.lean','QuantumBlockEncoding/HermiteTransferCores'),
    @('QuantumBlockEncoding/MatrixProductChain.lean','QuantumBlockEncoding/MatrixProductChain'),
    @('QuantumBlockEncoding/StoredMatrixProductChain.lean','QuantumBlockEncoding/StoredMatrixProductChain'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-producer/ActualDecomposition.lean','ActualDecomposition')
  )
  $taskBindings = @{}
  foreach ($taskSource in $taskSources) {
    $taskBindings[$taskSource[0]] = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource[0]).Hash.ToLower()
  }
  foreach ($taskFile in @('lean-toolchain','lake-manifest.json','tasks/SP-HERMITE-POLY-002.md', 'experiments/hermite-polynomial/precision/piecewise-kernel-producer/statement-seal-v1.json')) {
    $taskBindings[$taskFile] = (Get-FileHash -Algorithm SHA256 -LiteralPath $taskFile).Hash.ToLower()
  }
  $taskBindings | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/pre-gate-bindings.json"
  foreach ($taskSource in $taskSources) {
    Write-Output "BEGIN $($taskSource[0])"
    lake env lean -o "$PSScriptRoot/.cache/$($taskSource[1]).olean" $taskSource[0]
    if ($LASTEXITCODE -ne 0) { throw "Whole-source gate failed: $($taskSource[0])" }
    Write-Output "PASS $($taskSource[0])"
  }
  foreach ($taskFile in $taskBindings.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskFile).Hash.ToLower() -ne $taskBindings[$taskFile]) {
      throw "Binding changed: $taskFile"
    }
  }
  Write-Output 'ALL PRE-GATE BINDINGS UNCHANGED'
} finally {
  $env:LEAN_PATH = $taskPriorLeanPath
  Pop-Location
}
