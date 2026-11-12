$ErrorActionPreference = 'Stop'
$reviewRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$reviewPriorLeanPath = $env:LEAN_PATH
Push-Location -LiteralPath $reviewRepoRoot
try {
  $reviewCache = Join-Path $PSScriptRoot '.cache'
  New-Item -ItemType Directory -Force -Path $reviewCache | Out-Null
  $env:LEAN_PATH = "$reviewCache;$reviewPriorLeanPath"
  $reviewSources = @(
    @('FiniteExp', 'finite-exp/FiniteExp.lean'),
    @('RadiusSupplier', 'radius-supplier/RadiusSupplier.lean'),
    @('CoefficientRange', 'coefficient-range/CoefficientRange.lean'),
    @('NormalizationStability', 'NormalizationStability.lean'),
    @('RadiusStability', 'radius-stability/RadiusStability.lean'),
    @('GlobalRadiusBudget', 'global-radius-budget/GlobalRadiusBudget.lean')
  )
  foreach ($reviewSource in $reviewSources) {
    Write-Output ("FULL_SOURCE " + $reviewSource[1])
    lake env lean -o (Join-Path $reviewCache ($reviewSource[0] + '.olean')) (Join-Path 'experiments/hermite-polynomial/precision' $reviewSource[1])
    if ($LASTEXITCODE -ne 0) { throw ('Independent full source failed: ' + $reviewSource[1]) }
  }
  foreach ($reviewConsumer in @('finite-exp/ConsumerChecks.lean', 'global-radius-budget/ConsumerChecks.lean', 'bridge-review-c14/AnalyticDiscriminators.lean')) {
    Write-Output ("CONSUMER " + $reviewConsumer)
    lake env lean (Join-Path 'experiments/hermite-polynomial/precision' $reviewConsumer)
    if ($LASTEXITCODE -ne 0) { throw ('Independent consumer failed: ' + $reviewConsumer) }
  }
} finally {
  $env:LEAN_PATH = $reviewPriorLeanPath
  Pop-Location
}
