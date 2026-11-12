$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskPriorLeanPath=$env:LEAN_PATH
Push-Location -LiteralPath $taskRepoRoot
try {
  $env:LEAN_PATH="$PSScriptRoot/.cache"
  $taskOld=Get-Content -Raw -LiteralPath "$PSScriptRoot/pre-gate-bindings.json" | ConvertFrom-Json -AsHashtable
  foreach ($taskPath in $taskOld.Keys) {
    if ($taskPath -notmatch 'ActualDecomposition.lean$') {
      if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskOld[$taskPath]) {
        throw "Old prefix source mismatch: $taskPath"
      }
    }
  }
  $taskSources=@(
    @('experiments/hermite-polynomial/precision/global-radius-budget/GlobalRadiusBudget.lean','GlobalRadiusBudget'),
    @('experiments/hermite-polynomial/precision/piecewise-source-budget/PiecewiseSourceBudget.lean','PiecewiseSourceBudget'),
    @('QuantumBlockEncoding/HermiteTransferCores.lean','QuantumBlockEncoding/HermiteTransferCores'),
    @('QuantumBlockEncoding/MatrixProductChain.lean','QuantumBlockEncoding/MatrixProductChain'),
    @('QuantumBlockEncoding/StoredMatrixProductChain.lean','QuantumBlockEncoding/StoredMatrixProductChain'),
    @('experiments/hermite-polynomial/precision/piecewise-kernel-producer/ActualDecomposition.lean','ActualDecomposition')
  )
  $taskBindings=@{}
  foreach ($taskSource in $taskSources) {
    $taskBindings[$taskSource[0]]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskSource[0]).Hash.ToLower()
  }
  Get-ChildItem -Recurse -File -LiteralPath "$PSScriptRoot/.cache" | ForEach-Object {
    $taskBindings[$_.FullName]=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()
  }
  $taskBindings | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/pre-tail-v2-bindings.json"
  foreach ($taskSource in $taskSources) {
    Write-Output "BEGIN $($taskSource[0])"
    lake env lean -o "$PSScriptRoot/.cache/$($taskSource[1]).olean" $taskSource[0]
    if ($LASTEXITCODE -ne 0) { throw "Tail source failed: $($taskSource[0])" }
    Write-Output "PASS $($taskSource[0])"
  }
  foreach ($taskPath in $taskBindings.Keys) {
    if ($taskPath -notmatch '.olean$') {
      if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskPath]) { throw "Binding changed: $taskPath" }
    }
  }
  Write-Output 'TAIL V2 INPUT BINDINGS UNCHANGED'
} finally {
  $env:LEAN_PATH=$taskPriorLeanPath
  Pop-Location
}
