$ErrorActionPreference = 'Stop'
$reviewRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$reviewPriorLeanPath = $env:LEAN_PATH
Push-Location -LiteralPath $reviewRepoRoot
try {
  $reviewCache = Join-Path $PSScriptRoot '.cache'
  New-Item -ItemType Directory -Force -Path $reviewCache | Out-Null
  $env:LEAN_PATH = "$reviewCache;$reviewPriorLeanPath"
  lake env lean -o (Join-Path $reviewCache 'FiniteTrig.olean') experiments/hermite-polynomial/precision/finite-trig/FiniteTrig.lean
  if ($LASTEXITCODE -ne 0) { throw 'Independent full finite trig dependency failed' }
  lake env lean -o (Join-Path $reviewCache 'SavedRyInterval.olean') experiments/hermite-polynomial/precision/saved-ry-interval/SavedRyInterval.lean
  if ($LASTEXITCODE -ne 0) { throw 'Independent full signed RY provider failed' }
  lake env lean experiments/hermite-polynomial/precision/saved-ry-interval/ConsumerChecks.lean
  if ($LASTEXITCODE -ne 0) { throw 'Independent actual saved RY consumer failed' }
  lake env lean experiments/hermite-polynomial/precision/bridge-review-c14/RyDiscriminators.lean
  if ($LASTEXITCODE -ne 0) { throw 'Independent RY kernel discriminator failed' }
  .venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-ry-interval/test_saved_ry_interval.py -v
  if ($LASTEXITCODE -ne 0) { throw 'Actual saved RY exact finite diagnostics failed' }
} finally {
  $env:LEAN_PATH = $reviewPriorLeanPath
  Pop-Location
}
