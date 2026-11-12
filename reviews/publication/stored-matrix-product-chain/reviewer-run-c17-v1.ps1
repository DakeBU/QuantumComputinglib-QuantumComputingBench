param([string]$Version = 'v1')
$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8
$prefix = 'reviews/publication/stored-matrix-product-chain/reviewer-'
$receiptPath = $prefix + 'receipt-c17-' + $Version + '.json'
if (Test-Path -LiteralPath $receiptPath) { throw 'Frozen receipt already exists; replay refused.' }
$targetPath = 'QuantumBlockEncoding/StoredMatrixProductChain.lean'
$packetPath = $prefix + 'comparison-packet.json'
$packet = Get-Content -LiteralPath $packetPath -Raw -Encoding utf8 | ConvertFrom-Json
foreach ($pin in @(@($targetPath,$packet.module_sha256),@($packet.source_path,$packet.source_sha256),
    @($packet.source_first_path,$packet.source_first_sha256),@($packet.decoder_artifact,$packet.decoder_artifact_sha256),
    @($packet.decoder_evidence,$packet.decoder_evidence_sha256))) {
  if ((Get-FileHash -LiteralPath $pin[0] -Algorithm SHA256).Hash.ToLower() -ne $pin[1]) { throw ('Binding mismatch: '+$pin[0]) }
}
$target = Get-Content -LiteralPath $targetPath -Raw -Encoding utf8
$decls = @([regex]::Matches($target,'(?m)^(?:@\[simp\] )?(?:noncomputable )?(def|theorem) ([A-Za-z][A-Za-z0-9_]*)') | ForEach-Object {
  [ordered]@{ fullName='QuantumBlockEncoding.StoredMatrixProductChain.'+$_.Groups[2].Value; kind=$_.Groups[1].Value }
})
if ($decls.Count -ne 29) { throw 'Actual source public inventory changed.' }
$seen = [System.Collections.Generic.HashSet[string]]::new()
$todo = [System.Collections.Generic.Queue[string]]::new()
$todo.Enqueue($targetPath)
$external = [System.Collections.Generic.HashSet[string]]::new()
while ($todo.Count) {
  $p = $todo.Dequeue()
  if (-not $seen.Add($p)) { continue }
  foreach ($m in [regex]::Matches((Get-Content -LiteralPath $p -Raw -Encoding utf8), '(?m)^import\s+(\S+)')) {
    $name = $m.Groups[1].Value
    $q = $name.Replace('.','/') + '.lean'
    if (Test-Path -LiteralPath $q) { $todo.Enqueue($q) } else { [void]$external.Add($name) }
  }
}
$probePath = $prefix+'probes-c17-'+$Version+'.lean'
$paths = @($seen) + @($packetPath,$packet.source_path,$packet.source_first_path,$packet.decoder_artifact,
  $packet.decoder_evidence,'lean-toolchain','lake-manifest.json','lakefile.lean',
  'website/scripts/check_research_publications.py',$probePath,($prefix+'run-c17-v1.ps1'))
foreach ($p in @($seen)) {
  if ($p -eq $targetPath) { continue }
  $o = '.lake/build/lib/lean/' + $p.Replace('.lean','.olean')
  if (Test-Path -LiteralPath $o) { $paths += $o }
}
foreach ($name in $external) {
  foreach ($p in @(('.lake/packages/mathlib/'+$name.Replace('.','/')+'.lean'),
    ('.lake/packages/mathlib/.lake/build/lib/lean/'+$name.Replace('.','/')+'.olean'))) {
    if (Test-Path -LiteralPath $p) { $paths += $p }
  }
}
function HashRows($list) {
  @($list | Sort-Object -Unique | ForEach-Object { [ordered]@{path=$_; sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLower()} })
}
$before = HashRows $paths
$checks = ($decls | ForEach-Object { '#check '+$_.fullName+"`n#print axioms "+$_.fullName }) -join "`n"
$whole = $target + "`n" + $checks + "`n" + (Get-Content -LiteralPath $probePath -Raw -Encoding utf8)
$assemblySha = [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($utf8.GetBytes($whole))).ToLower()
$start = [DateTime]::UtcNow
$ErrorActionPreference = 'Continue'
$captured = $whole | & lake env lean --stdin 2>&1 | Out-String
$code = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
$elapsed = ([DateTime]::UtcNow-$start).TotalSeconds
$after = HashRows $paths
$changed = @($before | Where-Object { $p=$_.path; $sha=$_.sha256; -not ($after | Where-Object { $_.path -eq $p -and $_.sha256 -eq $sha }) })
$receipt = [ordered]@{
  schema_version=1; role='reviewer'; identity='/root/stored_matrix_source_reviewer_c17'; run_id='stored-matrix-source-reviewer-c17-'+$Version;
  binding_sha256=$packet.binding_sha256; packet_path=$packetPath;
  packet_sha256=(Get-FileHash -LiteralPath $packetPath -Algorithm SHA256).Hash.ToLower();
  target_sha256=$packet.module_sha256; source_first_sha256=$packet.source_first_sha256;
  command='lake env lean --stdin'; source_assembly_sha256=$assemblySha;
  source_assembly='Exact complete current target source, including imports and all private helpers, followed by independent source-derived 29 checks/axiom queries and reviewer probes. No target olean import; no -o output.';
  cache_scope='Project import-closure source/olean hashes and directly imported external Mathlib source/olean hashes before/after. Provider caches inherited, not freshly rebuilt. Not full transitive Mathlib audit or admission.';
  exit_code=$code; seconds=$elapsed; status=$(if($code -eq 0 -and $changed.Count -eq 0){'passed'}else{'excluded-failed-whole-module'});
  declaration_inventory=$decls; allowed_reads_before=$before; allowed_reads_after=$after; changed_context=$changed;
  stdout=$captured.Replace((Get-Location).Path,'<repo>')
}
# No files are written by this runner. The caller preserves this output via apply_patch.
$receipt | ConvertTo-Json -Depth 20
