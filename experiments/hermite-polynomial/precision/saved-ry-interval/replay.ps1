$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
    New-Item -ItemType Directory -Force -Path '.lake/saved-ry-interval-cache' | Out-Null
    $taskPreviousLeanPath = $env:LEAN_PATH
    $env:LEAN_PATH = "$taskRepoRoot/.lake/saved-ry-interval-cache;$taskRepoRoot/.lake/finite-trig-cache;$taskPreviousLeanPath"
    lake env lean -o .lake/saved-ry-interval-cache/SavedRyInterval.olean experiments/hermite-polynomial/precision/saved-ry-interval/SavedRyInterval.lean
    if ($LASTEXITCODE -ne 0) { throw 'Actual RY provider focused compilation failed' }
    lake env lean experiments/hermite-polynomial/precision/saved-ry-interval/ConsumerChecks.lean
    if ($LASTEXITCODE -ne 0) { throw 'Kernel consumers or axiom prints failed' }
    .venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-ry-interval/test_saved_ry_interval.py -v
    if ($LASTEXITCODE -ne 0) { throw 'Exact finite diagnostics failed' }
} finally {
    $env:LEAN_PATH = $taskPreviousLeanPath
    Pop-Location
}
