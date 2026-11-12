$ErrorActionPreference='Stop'
$reviewRepo=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../..')).Path
$receipt=Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'consumer-v2.json') | ConvertFrom-Json
$v1=Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'consumer-v1.json') | ConvertFrom-Json
$v1Hash=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot 'consumer-v1-source.txt')).Hash.ToLowerInvariant()
if ($v1Hash -ne $v1.bindings_before.'reviews/internal/c22-stored-supplier-review/IndependentConsumer.lean') { throw 'Retained failed source bytes do not match v1 receipt' }
$changed=@()
foreach ($entry in $receipt.bindings_after.PSObject.Properties) {
 $current=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $reviewRepo $entry.Name)).Hash.ToLowerInvariant()
 if ($current -ne $entry.Value) { $changed += $entry.Name }
}
if ($changed.Count -ne 0) { throw "Inputs changed since successful consumer: $($changed -join ', ')" }
$artifacts=[ordered]@{}
foreach ($file in (Get-ChildItem -LiteralPath $PSScriptRoot -File | Where-Object { $_.Name -ne 'final-bindings.json' })) {
 $artifacts["reviews/internal/c22-stored-supplier-review/$($file.Name)"]=(Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash.ToLowerInvariant()
}
$frozen=[ordered]@{schema='c22-independent-freeze-v1';frozen_utc=[DateTime]::UtcNow.ToString('o');verdict='ACCEPT_INTERNAL_LOCAL_SEMANTICS_AND_PARTIAL_LEDGER';direction_fingerprint='C22_INDEPENDENT_SAME_OBJECT_AND_COST_BOUNDARY';successful_consumer_exit=$receipt.lean_exit;successful_consumer_input_changes=$receipt.changed_inputs;successful_input_binding_recheck='unchanged';failed_source_byte_binding='matches consumer-v1';review_owned_artifacts=$artifacts;source_bindings=$receipt.bindings_after;admission_boundary='Internal provider/checkpoint semantics and partial ledger only. No full scalar runtime, finite-bit, publication, quantum root, repository gate, main admission or Exposition Seal claimed.'}
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'final-bindings.json'),($frozen | ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
Write-Output "Frozen artifacts=$($artifacts.Count); successful inputs unchanged; failed-source bytes retained exactly"
