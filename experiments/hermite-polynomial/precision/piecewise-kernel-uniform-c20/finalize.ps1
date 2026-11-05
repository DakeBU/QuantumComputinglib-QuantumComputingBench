$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
Push-Location -LiteralPath $taskRepoRoot
try {
  $taskBindings=Get-Content -Raw -LiteralPath "$PSScriptRoot/pre-gate-bindings.json" | ConvertFrom-Json -AsHashtable
  foreach ($taskPath in $taskBindings.Keys) {
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower() -ne $taskBindings[$taskPath]) { throw "Frozen proof/source binding changed:$taskPath" }
  }
  $taskFinal=Get-Content -Raw -LiteralPath "$PSScriptRoot/focused-v1.raw.log"
  if ($taskFinal -notmatch 'ALL PRE-GATE SOURCE/SEAL/INHERITED BINDINGS UNCHANGED' -or $taskFinal -match 'sorryAx|error:') { throw 'Final whole source/consumer gate failed' }
  foreach ($taskLean in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*.lean') {
    $taskText=Get-Content -Raw -LiteralPath $taskLean.FullName
    if ($taskText -match '\bsorry\b|\badmit\b|\bnative_decide\b|\bunsafe\b|\bofReduceBool\b|(?m)^\s*axiom\b') { throw 'Forbidden Lean proof content' }
  }
  $taskRaw=@{}
  foreach ($taskLog in Get-ChildItem -File -LiteralPath $PSScriptRoot -Filter '*.raw.log') {
    $taskRawHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskLog.FullName).Hash.ToLower()
    $taskPublic=$taskLog.Name.Replace('.raw.log','.public-v1.log')
    $taskText=(Get-Content -Raw -LiteralPath $taskLog.FullName).Replace($taskRepoRoot,'.')
    if ($taskText -match '[A-Za-z]:[\\/]') { throw 'Nonrepository drive path in derivative' }
    $taskText | Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot $taskPublic)
    $taskRaw[$taskLog.Name]=@{raw_sha256=$taskRawHash;private_ignored=$true;public_derivative=$taskPublic;public_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot $taskPublic)).Hash.ToLower()}
  }
  $taskRaw | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/private-raw-provenance.json"
  $taskArtifacts=@{}
  $taskCaches=@{}
  Get-ChildItem -Recurse -File -LiteralPath $PSScriptRoot | Where-Object { $_.Name -ne 'final-binding-manifest.json' -and $_.Name -notlike '*.raw.log' } | ForEach-Object {
    $taskRelative=$_.FullName.Substring($PSScriptRoot.Length+1).Replace('\','/')
    $taskHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLower()
    if ($taskRelative.StartsWith('.cache/')) { $taskCaches[$taskRelative]=$taskHash } else { $taskArtifacts[$taskRelative]=$taskHash }
  }
  @{proof_source_inherited_bindings=$taskBindings;artifact_hashes=$taskArtifacts;ignored_cache_hashes=$taskCaches;raw_provenance='private-raw-provenance.json';bindings_unchanged=$true;scientific_ROOT=$false;all_writes_stopped=$true} | ConvertTo-Json -Depth 20 | Set-Content -Encoding utf8 -LiteralPath "$PSScriptRoot/final-binding-manifest.json"
  function Assert-TaskStrings($taskValue) {
    if ($taskValue -is [string]) { if ($taskValue -match '[A-Za-z]:[\\/]') { throw 'Drive path in decoded public JSON' } }
    elseif ($taskValue -is [System.Collections.IDictionary]) { foreach ($taskKey in $taskValue.Keys) { Assert-TaskStrings ([string]$taskKey); Assert-TaskStrings $taskValue[$taskKey] } }
    elseif ($taskValue -is [System.Collections.IEnumerable]) { foreach ($taskItem in $taskValue) { Assert-TaskStrings $taskItem } }
  }
  foreach ($taskFile in Get-ChildItem -File -LiteralPath $PSScriptRoot | Where-Object { $_.Name -notlike '*.raw.log' }) {
    $taskText=Get-Content -Raw -LiteralPath $taskFile.FullName
    if ($taskText -match '[A-Za-z]:[\\/]') { throw "Drive path in public file:$($taskFile.Name)" }
    if ($taskFile.Extension -eq '.json') { Assert-TaskStrings ($taskText | ConvertFrom-Json -AsHashtable) }
  }
  Write-Output "RESULT SHA256 $($taskArtifacts['result.json'])"
  Write-Output "COMPARATOR SHA256 $($taskArtifacts['UniformComparison.lean'])"
  Write-Output "TRANSLATION SHA256 $($taskArtifacts['UniformTranslation.lean'])"
  Write-Output "THRESHOLDS SHA256 $($taskArtifacts['UniformThresholds.lean'])"
  Write-Output "MANIFEST SHA256 $((Get-FileHash -Algorithm SHA256 -LiteralPath "$PSScriptRoot/final-binding-manifest.json").Hash.ToLower())"
  Write-Output 'ALL WRITES STOPPED'
} finally { Pop-Location }
