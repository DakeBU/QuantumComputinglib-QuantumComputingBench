$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
    New-Item -ItemType Directory -Force -Path '.lake/finite-trig-cache' | Out-Null
    $taskPreviousLeanPath = $env:LEAN_PATH
    $env:LEAN_PATH = "$taskRepoRoot/.lake/finite-trig-cache;$taskPreviousLeanPath"
    lake env lean -o .lake/finite-trig-cache/FiniteTrig.olean experiments/hermite-polynomial/precision/finite-trig/FiniteTrig.lean
    if ($LASTEXITCODE -ne 0) { throw 'Scalar full-source compilation failed' }
    lake env lean -o .lake/finite-trig-cache/FiniteTrigProducer.olean experiments/hermite-polynomial/precision/finite-trig/FiniteTrigProducer.lean
    if ($LASTEXITCODE -ne 0) { throw 'Finite producer full-source compilation failed' }
    lake env lean experiments/hermite-polynomial/precision/finite-trig/FiniteTrigCheck.lean
    if ($LASTEXITCODE -ne 0) { throw 'Consumer/axiom regression compilation failed' }
    .venv/Scripts/python.exe -m unittest discover -s experiments/hermite-polynomial/precision/finite-trig -p test_finite_trig.py -v
    if ($LASTEXITCODE -ne 0) { throw 'Exact rational executable tests failed' }
} finally {
    $env:LEAN_PATH = $taskPreviousLeanPath
    Pop-Location
}
