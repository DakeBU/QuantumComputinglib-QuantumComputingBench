$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
$taskPreviousLeanPath = $env:LEAN_PATH
try {
    New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache" | Out-Null
    $env:LEAN_PATH = "$PSScriptRoot/.cache;$taskPreviousLeanPath"
    New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache/QuantumBlockEncoding" | Out-Null
    lake env lean -o "$PSScriptRoot/.cache/QuantumBlockEncoding/HermitePolynomial.olean" QuantumBlockEncoding/HermitePolynomial.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full literal original Hermite source failed' }
    lake env lean -o "$PSScriptRoot/.cache/CoefficientRange.olean" experiments/hermite-polynomial/precision/coefficient-range/CoefficientRange.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full coefficient-range provider failed' }
    lake env lean -o "$PSScriptRoot/.cache/FiniteExp.olean" experiments/hermite-polynomial/precision/finite-exp/FiniteExp.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full original finite exponential provider failed' }
    lake env lean -o "$PSScriptRoot/.cache/FiniteExpDegree.olean" experiments/hermite-polynomial/precision/finite-exp-degree/FiniteExpDegree.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full uniform degree provider failed' }
    lake env lean -o "$PSScriptRoot/.cache/FiniteMiddleSource.olean" experiments/hermite-polynomial/precision/finite-middle-source/FiniteMiddleSource.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full middle source provider failed' }
    lake env lean experiments/hermite-polynomial/precision/finite-middle-source/ConsumerChecks.lean
    if ($LASTEXITCODE -ne 0) { throw 'Full rational original-source consumer and discriminators failed' }
} finally {
    $env:LEAN_PATH = $taskPreviousLeanPath
    Pop-Location
}
