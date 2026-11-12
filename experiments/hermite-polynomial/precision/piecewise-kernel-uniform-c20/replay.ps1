$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskPriorLeanPath=$env:LEAN_PATH
Push-Location -LiteralPath $taskRepoRoot
try {
  New-Item -ItemType Directory -Force -Path "$PSScriptRoot/.cache/QuantumBlockEncoding" | Out-Null
  $env:LEAN_PATH="$PSScriptRoot/.cache"
  $taskSources=@(
    @('QuantumBlockEncoding/HermiteTransferCores.lean','QuantumBlockEncoding/HermiteTransferCores'),
    @('QuantumBlockEncoding/MatrixProductChain.lean','QuantumBlockEncoding/MatrixProductChain'),
    @('QuantumBlockEncoding/StoredMatrixProductChain.lean','QuantumBlockEncoding/StoredMatrixProductChain'),
    @('QuantumBlockEncoding/StoredBinaryCoordinates.lean','QuantumBlockEncoding/StoredBinaryCoordinates'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformComparison.lean','UniformComparison'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformTranslation.lean','UniformTranslation'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/UniformThresholds.lean','UniformThresholds'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/ConsumerChecks.lean','ConsumerChecks')
  )
  $taskBindings=@{}
  foreach ($taskSource in $taskSources) { $taskBindings[$taskSource[0]]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource[0]).Hash.ToLower() }
  foreach ($taskPath in @('lean-toolchain','lake-manifest.json','tasks/SP-HERMITE-POLY-002.md','experiments/hermite-polynomial/precision/piecewise-kernel-producer/ActualDecomposition.lean','experiments/hermite-polynomial/precision/piecewise-kernel-producer/producer.py','experiments/hermite-polynomial/precision/piecewise-kernel-producer/result.json','experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseSourceBudget.lean','experiments/hermite-polynomial/precision/piecewise-source-budget/result.json','experiments/hermite-polynomial/precision/piecewise-tt-next-design-c17.json','reports/process-memory.json')) {
    $taskBindings[$taskPath]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
  }
  foreach ($taskSeal in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*seal*.json') {
    $taskRelative='experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/'+$taskSeal.Name
    $taskBindings[$taskRelative]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskSeal.FullName).Hash.ToLower()
  }
  $taskBindings | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/pre-gate-bindings.json"
  foreach ($taskSource in $taskSources) {
    Write-Output "BEGIN $($taskSource[0])"
    lake env lean -o "$PSScriptRoot/.cache/$($taskSource[1]).olean" $taskSource[0]
    if ($LASTEXITCODE -ne 0) { throw "Fresh source failed:$($taskSource[0])" }
    Write-Output "PASS $($taskSource[0])"
  }
  foreach ($taskPath in $taskBindings.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskPath]) { throw "Binding changed:$taskPath" }
  }
  Write-Output 'ALL PRE-GATE SOURCE/SEAL/INHERITED BINDINGS UNCHANGED'
} finally {
  $env:LEAN_PATH=$taskPriorLeanPath
  Pop-Location
}
