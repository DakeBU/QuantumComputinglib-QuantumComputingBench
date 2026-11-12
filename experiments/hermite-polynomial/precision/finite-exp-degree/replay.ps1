$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
$taskPreviousLeanPath = $env:LEAN_PATH
try {
    New-Item -ItemType Directory -Force -Path '.lake/finite-exp-cache' | Out-Null
    $env:LEAN_PATH = "$taskRepoRoot/.lake/finite-exp-cache;$taskPreviousLeanPath"
    lake env lean -o .lake/finite-exp-cache/FiniteExp.olean experiments/hermite-polynomial/precision/finite-exp/FiniteExp.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full original finite exponential provider compilation failed' }
    lake env lean -o .lake/finite-exp-cache/FiniteExpDegree.olean experiments/hermite-polynomial/precision/finite-exp-degree/FiniteExpDegree.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full uniform degree provider compilation failed' }
    lake env lean experiments/hermite-polynomial/precision/finite-exp-degree/ConsumerChecks.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full actual scalar consumers and regressions failed' }
} finally {
    $env:LEAN_PATH = $taskPreviousLeanPath
    Pop-Location
}
