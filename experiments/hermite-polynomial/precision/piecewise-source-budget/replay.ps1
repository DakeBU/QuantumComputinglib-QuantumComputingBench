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
    @('experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseSourceBudget.lean','PiecewiseSourceBudget')
  )
  foreach ($taskSource in $taskSources) {
    Write-Output "BEGIN $($taskSource[0])"
    lake env lean -o "$PSScriptRoot/.cache/$($taskSource[1]).olean" $taskSource[0]
    if ($LASTEXITCODE -ne 0) { throw "Whole-source gate failed: $($taskSource[0])" }
    Write-Output "PASS $($taskSource[0])"
  }
  Write-Output 'BEGIN experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseConsumerChecks.lean'
  lake env lean experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseConsumerChecks.lean
  if ($LASTEXITCODE -ne 0) { throw 'Whole original-amplitude consumer failed' }
  Write-Output 'PASS experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseConsumerChecks.lean'
} finally {
  $env:LEAN_PATH = $taskPriorLeanPath
  Pop-Location
}
