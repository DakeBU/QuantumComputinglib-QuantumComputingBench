$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
$taskPreviousLeanPath = $env:LEAN_PATH
try {
    New-Item -ItemType Directory -Force -Path '.lake/finite-exp-cache' | Out-Null
    $env:LEAN_PATH = "$taskRepoRoot/.lake/finite-exp-cache;$taskPreviousLeanPath"
    lake env lean -o .lake/finite-exp-cache/FiniteExp.olean experiments/hermite-polynomial/precision/finite-exp/FiniteExp.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full finite exponential provider compilation failed' }
    lake env lean experiments/hermite-polynomial/precision/finite-exp/ConsumerChecks.lean
    if ($LASTEXITCODE -ne 0) { throw 'Actual Hermite scalar consumers or regressions failed' }
} finally {
    $env:LEAN_PATH = $taskPreviousLeanPath
    Pop-Location
}
