$ErrorActionPreference = 'Stop'
$taskPriorLeanPath = $env:LEAN_PATH
try {
  $env:LEAN_PATH = 'experiments/hermite-polynomial/precision/global-radius-budget;.lake/radius-supplier-cache;.lake/radius-stability-cache;' + $taskPriorLeanPath
  lake env lean -o experiments/hermite-polynomial/precision/global-radius-budget/GlobalRadiusBudget.olean experiments/hermite-polynomial/precision/global-radius-budget/GlobalRadiusBudget.lean
  if ($LASTEXITCODE -ne 0) { throw 'Global radius provider failed' }
  lake env lean experiments/hermite-polynomial/precision/global-radius-budget/ConsumerChecks.lean
  if ($LASTEXITCODE -ne 0) { throw 'Original target consumer failed' }
} finally {
  $env:LEAN_PATH = $taskPriorLeanPath
}
