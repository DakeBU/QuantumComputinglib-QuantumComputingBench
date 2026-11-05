$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
  $taskOld=Get-Content -Raw -LiteralPath "$PSScriptRoot/pre-gate-bindings.json" | ConvertFrom-Json -AsHashtable
  $taskTail=Get-Content -Raw -LiteralPath "$PSScriptRoot/pre-tail-v2-bindings.json" | ConvertFrom-Json -AsHashtable
  foreach ($taskPath in $taskOld.Keys) {
    if ($taskPath -notmatch 'ActualDecomposition.lean$') {
      if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskOld[$taskPath]) { throw "Frozen prefix mismatch: $taskPath" }
    }
  }
  foreach ($taskPath in $taskTail.Keys) {
    if ($taskPath -notmatch '.olean$') {
      if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskTail[$taskPath]) { throw "Frozen tail mismatch: $taskPath" }
    }
  }
  $taskProof=Get-Content -Raw -LiteralPath "$PSScriptRoot/ActualDecomposition.lean"
  if ($taskProof -match '\bsorry\b|\badmit\b|\bnative_decide\b|\bunsafe\b|\bofReduceBool\b|(?m)^\s*axiom\b') { throw 'Forbidden Lean content' }
  $taskFocused=Get-Content -Raw -LiteralPath "$PSScriptRoot/focused-v2.log"
  if ($taskFocused -notmatch 'TAIL V2 INPUT BINDINGS UNCHANGED' -or $taskFocused -match 'sorryAx|error:') { throw 'Focused gate receipt failed' }
  $taskFinite=Get-Content -Raw -LiteralPath "$PSScriptRoot/finite-v3.log"
  if ($taskFinite -notmatch 'Ran 6 tests' -or $taskFinite -notmatch '\bOK\b' -or $taskFinite -match 'FAILED|ERROR') { throw 'Finite gate receipt failed' }
  $taskPacket=Get-Content -Raw -LiteralPath "$PSScriptRoot/stored-object-v1.json" | ConvertFrom-Json -AsHashtable
  $taskResult=Get-Content -Raw -LiteralPath "$PSScriptRoot/result.json" | ConvertFrom-Json -AsHashtable
  foreach ($taskOp in $taskPacket.generation_schedule_counts.Keys) {
    if ($taskPacket.generation_schedule_counts[$taskOp] -ne $taskResult.operation_model.saved_D90_width3.generation[$taskOp]) { throw "Finite generation count mismatch:$taskOp" }
  }
  $taskArtifacts=@{}
  $taskCaches=@{}
  $taskPrivate=@('focused-v1.log','focused-v2.log','pre-tail-v2-bindings.json')
  Get-ChildItem -Recurse -File -LiteralPath $PSScriptRoot | Where-Object { $_.Name -ne 'final-binding-manifest.json' -and $_.Name -notin $taskPrivate -and $_.FullName -notmatch '__pycache__' } | ForEach-Object {
    $taskRelative=$_.FullName.Substring($PSScriptRoot.Length+1).Replace('\','/')
    $taskHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()
    if ($taskRelative -match '^.cache/') { $taskCaches[$taskRelative]=$taskHash } else { $taskArtifacts[$taskRelative]=$taskHash }
  }
  $taskSources=@{}
  foreach ($taskPath in $taskOld.Keys) { $taskSources[$taskPath]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() }
  foreach ($taskPath in @('experiments/hermite-polynomial/precision/piecewise-source-budget/result.json','experiments/hermite-polynomial/precision/piecewise-tt-next-design-c17.json','experiments/hermite-polynomial/precision/source-stage-review-c17/independent-audit.json','reports/process-memory.json')) {
    $taskSources[$taskPath]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
  }
  $taskManifest=@{source_bindings=$taskSources;artifact_hashes=$taskArtifacts;ignored_cache_hashes=$taskCaches;prefix_tail_bindings_verified=$true;proof_roots=3;finite_test_methods=6;scientific_ROOT=$false;all_writes_stopped=$true}
  $taskManifest | ConvertTo-Json -Depth 20 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/final-binding-manifest.json"
  function Assert-TaskRelativeStrings($taskValue) {
    if ($taskValue -is [string]) {
      if ($taskValue -match '[A-Za-z]:[\\/]') { throw 'Absolute drive path in decoded public JSON string' }
    } elseif ($taskValue -is [System.Collections.IDictionary]) {
      foreach ($taskKey in $taskValue.Keys) { Assert-TaskRelativeStrings ([string]$taskKey); Assert-TaskRelativeStrings $taskValue[$taskKey] }
    } elseif ($taskValue -is [System.Collections.IEnumerable]) {
      foreach ($taskItem in $taskValue) { Assert-TaskRelativeStrings $taskItem }
    }
  }
  Get-ChildItem -File -LiteralPath $PSScriptRoot | Where-Object { $_.Name -notin $taskPrivate } | ForEach-Object {
    $taskText=Get-Content -Raw -LiteralPath $_.FullName
    if ($taskText -match '[A-Za-z]:[\\/]') { throw "Drive path in public artifact:$($_.Name)" }
    if ($_.Extension -eq '.json') { Assert-TaskRelativeStrings ($taskText | ConvertFrom-Json -AsHashtable) }
  }
  Write-Output "RESULT SHA256 $($taskArtifacts['result.json'])"
  Write-Output "LEAN SHA256 $($taskArtifacts['ActualDecomposition.lean'])"
  Write-Output "PRODUCER SHA256 $($taskArtifacts['producer.py'])"
  Write-Output "STORED OBJECT SHA256 $($taskArtifacts['stored-object-v1.json'])"
  Write-Output "MANIFEST SHA256 $((Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/final-binding-manifest.json").Hash.ToLower())"
  Write-Output 'ALL WRITES STOPPED'
} finally { Pop-Location }
