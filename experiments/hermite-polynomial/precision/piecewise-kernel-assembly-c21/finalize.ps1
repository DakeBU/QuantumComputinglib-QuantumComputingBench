$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
  $taskBindings=Get-Content -Raw -LiteralPath "$PSScriptRoot/pre-gate-bindings.json" | ConvertFrom-Json -AsHashtable
  foreach ($taskSection in @('sources','frozen_inherited')) {
    foreach ($taskPath in $taskBindings[$taskSection].Keys) {
      if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskSection][$taskPath]) { throw "Proof/frozen binding changed:$taskPath" }
    }
  }
  $taskInheritedSourceBindings=@{}
  foreach ($taskPriorReceipt in @('experiments/hermite-polynomial/precision/piecewise-kernel-producer/final-binding-manifest.json','experiments/hermite-polynomial/precision/piecewise-kernel-uniform-c20/pre-gate-bindings.json')) {
    $taskPrior=Get-Content -Raw -LiteralPath $taskPriorReceipt | ConvertFrom-Json -AsHashtable
    if ($taskPrior.ContainsKey('source_bindings')) { $taskPrior=$taskPrior['source_bindings'] }
    foreach ($taskPath in $taskPrior.Keys) {
      if ($taskPath.EndsWith('.lean') -or $taskPath -eq 'lean-toolchain' -or $taskPath -eq 'lake-manifest.json') {
        $taskCurrent=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
        if ($taskCurrent -ne $taskPrior[$taskPath]) { throw "Inherited proof input differs from frozen supplier receipt:$taskPath" }
        $taskInheritedSourceBindings[$taskPath]=$taskCurrent
      }
    }
  }
  $taskFinal=Get-Content -Raw -LiteralPath "$PSScriptRoot/focused-v1.raw.log"
  if ($taskFinal -notmatch 'ALL PRE-GATE SOURCE/SEAL/FROZEN BINDINGS UNCHANGED' -or $taskFinal -match 'sorryAx|error:') { throw 'Final 19-source gate failed' }
  $taskPassCount=([regex]::Matches($taskFinal,'(?m)^PASS ')).Count
  if ($taskPassCount -ne 19) { throw "Expected 19 fresh source passes; found $taskPassCount" }
  foreach ($taskLean in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*.lean') {
    if ((Get-Content -Raw -LiteralPath $taskLean.FullName) -match '\bsorry\b|\badmit\b|\bnative_decide\b|\bunsafe\b|\bofReduceBool\b|(?m)^\s*axiom\b') { throw "Forbidden proof content:$($taskLean.Name)" }
  }
  $taskRaw=@{}
  foreach ($taskLog in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*.raw.log') {
    $taskPublic=$taskLog.Name.Replace('.raw.log','.public-v1.log')
    $taskText=(Get-Content -Raw -LiteralPath $taskLog.FullName).Replace($taskRepoRoot,'.').Replace($taskRepoRoot.Replace('\','/'),'.')
    if ($taskText -match '[A-Za-z]:[\\/]') { throw "Unexpected absolute path:$($taskLog.Name)" }
    $taskText | Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot $taskPublic)
    $taskRaw[$taskLog.Name]=@{raw_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskLog.FullName).Hash.ToLower();private_ignored=$true;public_derivative=$taskPublic;public_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot $taskPublic)).Hash.ToLower()}
  }
  $taskRaw | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/private-raw-provenance.json"
  $taskArtifacts=@{}
  $taskCaches=@{}
  foreach ($taskFile in Get-ChildItem -Recurse -File -LiteralPath $PSScriptRoot) {
    $taskRelative=$taskFile.FullName.Substring($PSScriptRoot.Length+1).Replace('\','/')
    if ($taskFile.Name -eq 'final-binding-manifest.json' -or $taskFile.Name -like '*.raw.log') { continue }
    $taskHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskFile.FullName).Hash.ToLower()
    if ($taskRelative.StartsWith('.cache/')) { $taskCaches[$taskRelative]=$taskHash } else { $taskArtifacts[$taskRelative]=$taskHash }
  }
  @{pre_gate_bindings=$taskBindings;inherited_source_equality_to_frozen_receipts=$taskInheritedSourceBindings;artifact_hashes=$taskArtifacts;ignored_cache_hashes=$taskCaches;raw_provenance='private-raw-provenance.json';fresh_source_passes=$taskPassCount;resolved_consumerchecks=@{source='experiments/hermite-polynomial/precision/finite-middle-source/ConsumerChecks.lean';cache='.cache/ConsumerChecks.olean';cache_sha256=$taskCaches['.cache/ConsumerChecks.olean'];c20_consumerchecks_not_selected=$true};scientific_ROOT=$false;bindings_unchanged=$true;all_writes_stopped=$true} | ConvertTo-Json -Depth 30 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/final-binding-manifest.json"
  function Assert-TaskStrings($taskValue) {
    if ($taskValue -is [string]) { if ($taskValue -match '[A-Za-z]:[\\/]') { throw 'Drive path in decoded JSON' } }
    elseif ($taskValue -is [System.Collections.IDictionary]) { foreach ($taskKey in $taskValue.Keys) { Assert-TaskStrings ([string]$taskKey); Assert-TaskStrings $taskValue[$taskKey] } }
    elseif ($taskValue -is [System.Collections.IEnumerable]) { foreach ($taskItem in $taskValue) { Assert-TaskStrings $taskItem } }
  }
  foreach ($taskFile in Get-ChildItem -File -LiteralPath $PSScriptRoot | Where-Object { $_.Name -notlike '*.raw.log' }) {
    $taskText=Get-Content -Raw -LiteralPath $taskFile.FullName
    if ($taskText -match '[A-Za-z]:[\\/]') { throw "Drive path in public source/runner/log:$($taskFile.Name)" }
    if ($taskFile.Extension -eq '.json') { Assert-TaskStrings ($taskText | ConvertFrom-Json -AsHashtable) }
  }
  Write-Output "RESULT SHA256 $($taskArtifacts['result.json'])"
  Write-Output "ASSEMBLY SOURCE SHA256 $($taskArtifacts['ActualAssembly.lean'])"
  Write-Output "ASSEMBLY CACHE SHA256 $($taskCaches['.cache/ActualAssembly.olean'])"
  Write-Output "CONSUMER CACHE SHA256 $($taskCaches['.cache/AssemblyConsumerChecks.olean'])"
  Write-Output "MANIFEST SHA256 $((Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/final-binding-manifest.json").Hash.ToLower())"
  Write-Output 'ALL WRITES STOPPED'
} finally { Pop-Location }
