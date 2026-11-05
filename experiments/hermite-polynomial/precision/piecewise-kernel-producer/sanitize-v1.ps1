$ErrorActionPreference='Stop'
$taskRepoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskRawHashes=@{}
$taskDerivativeHashes=@{}
foreach ($taskLog in @('focused-v1.log','focused-v2.log')) {
  $taskPath=Join-Path $PSScriptRoot $taskLog
  $taskRawHashes[$taskLog]=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPath).Hash.ToLower()
  $taskPublicName=$taskLog.Replace('.log','.public-v1.log')
  $taskText=(Get-Content -Raw -LiteralPath $taskPath).Replace($taskRepoRoot,'.')
  if ($taskText -match '[A-Za-z]:[\\/]') { throw 'Nonrepository absolute path left in sanitized log' }
  $taskText | Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot $taskPublicName)
  $taskDerivativeHashes[$taskPublicName]=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot $taskPublicName)).Hash.ToLower()
}
$taskRawReceipt=Join-Path $PSScriptRoot 'pre-tail-v2-bindings.json'
$taskRawHashes['pre-tail-v2-bindings.json']=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskRawReceipt).Hash.ToLower()
$taskRaw=Get-Content -Raw -LiteralPath $taskRawReceipt | ConvertFrom-Json -AsHashtable
$taskRelative=@{}
foreach ($taskKey in $taskRaw.Keys) {
  $taskNewKey=$taskKey
  if ($taskKey.StartsWith($taskRepoRoot)) { $taskNewKey=$taskKey.Substring($taskRepoRoot.Length+1) }
  $taskNewKey=$taskNewKey.Replace('\','/')
  if ($taskNewKey -match '[A-Za-z]:[\\/]') { throw 'Nonrepository absolute binding key' }
  $taskRelative[$taskNewKey]=$taskRaw[$taskKey]
}
$taskPublicReceipt=Join-Path $PSScriptRoot 'pre-tail-v2-bindings.public-v1.json'
$taskRelative | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath $taskPublicReceipt
$taskDerivativeHashes['pre-tail-v2-bindings.public-v1.json']=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPublicReceipt).Hash.ToLower()
@{raw_private_ignored_hashes=$taskRawHashes;public_derivative_hashes=$taskDerivativeHashes;raw_byte_preserved=$true;sanitization='Replace actual repository root in log derivative only; convert repository cache binding keys to repository-relative. Raw logs/receipt remain unchanged and ignored.';original_v1_status='ENV_BLOCKED_INTERRUPTED';original_v2_status='TAIL_GATE_EXIT0'} | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot 'release-hygiene-v1.json')
Write-Output 'Sanitized derivatives generated; raw private byte hashes preserved.'
