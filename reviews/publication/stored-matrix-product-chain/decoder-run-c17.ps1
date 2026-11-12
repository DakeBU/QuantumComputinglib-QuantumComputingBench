param([string]$Version = 'v1')
$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8
$prefix = 'reviews/publication/stored-matrix-product-chain/decoder-'
$receiptPath = $prefix + 'receipt-c17-' + $Version + '.json'
if (Test-Path -LiteralPath $receiptPath) { throw 'Frozen receipt already exists; replay refused.' }
$targetPath = 'QuantumBlockEncoding/StoredMatrixProductChain.lean'
$target = Get-Content -LiteralPath $targetPath -Raw -Encoding utf8
$packetPath = 'reviews/publication/stored-matrix-product-chain/decoder-packet.json'
$packet = Get-Content -LiteralPath $packetPath -Raw -Encoding utf8 | ConvertFrom-Json
if ((Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash.ToLower() -ne $packet.module_sha256) { throw 'Target source binding mismatch' }
$decls = (Get-Content -LiteralPath 'web/library/declarations.json' -Raw -Encoding utf8 | ConvertFrom-Json).declarations | Where-Object source -EQ $targetPath | Select-Object fullName,kind,line
if ($decls.Count -ne 29) { throw 'Inventory changed' }
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
$paths = @($seen) + @('AGENTS.md','HARNESS.md','.agents/skills/qbe-substantive-worker/SKILL.md',
  'docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md',
  'docs/evidence-routed-memory-protocol.md','lean-toolchain','lake-manifest.json','lakefile.lean',
  'website/scripts/check_research_publications.py',$packetPath,($prefix+'probes-c17-'+$Version+'.lean'),($prefix+'run-c17.ps1'))
foreach ($p in @($seen)) {
  if ($p -eq $targetPath) { continue }
  $o = '.lake/build/lib/lean/' + $p.Replace('.lean','.olean')
  if (Test-Path -LiteralPath $o) { $paths += $o }
}
foreach ($name in $external) {
  $base = '.lake/packages/mathlib/' + $name.Replace('.','/')
  foreach ($p in @(($base+'.lean'),('.lake/packages/mathlib/.lake/build/lib/lean/'+$name.Replace('.','/')+'.olean'))) {
    if (Test-Path -LiteralPath $p) { $paths += $p }
  }
}
function HashRows($list) {
  @($list | Sort-Object -Unique | ForEach-Object { [ordered]@{path=$_; sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLower()} })
}
$before = HashRows $paths
$checks = ($decls | ForEach-Object { '#check ' + $_.fullName + "`n#print axioms " + $_.fullName }) -join "`n"
$probe = Get-Content -LiteralPath ($prefix+'probes-c17-'+$Version+'.lean') -Raw -Encoding utf8
$whole = $target + "`n" + $checks + "`n" + $probe
$start = [DateTime]::UtcNow
$oldPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$captured = $whole | & lake env lean --stdin 2>&1 | Out-String
$code = $LASTEXITCODE
$ErrorActionPreference = $oldPreference
$elapsed = ([DateTime]::UtcNow-$start).TotalSeconds
$sanitized = $captured.Replace((Get-Location).Path,'<repo>').Replace((Get-Location).Path.Replace('\','/'),'<repo>')
$sanitized = [regex]::Replace($sanitized,'[A-Za-z]:[\\/][^\r\n]*','<redacted-local-path>')
$after = HashRows $paths
$changed = @($before | Where-Object { $p=$_.path; $sha=$_.sha256; -not ($after | Where-Object { $_.path -eq $p -and $_.sha256 -eq $sha }) })
$receipt = [ordered]@{
  schema_version=1; identity='/root/stored_matrix_blind_c17'; run_id='stored-matrix-blind-c17-'+$Version;
  role='decoder'; source_blind=$true; binding_sha256=$packet.binding_sha256;
  packet_path=$packetPath; packet_sha256=(Get-FileHash -LiteralPath $packetPath -Algorithm SHA256).Hash.ToLower();
  target_sha256=$packet.module_sha256; command='lake env lean --stdin';
  source_assembly='Full unmodified target source including actual imports and private helpers, followed by own 29 checks and axiom queries, then own probes. No target olean import and no -o output.';
  cache_scope='Project provider oleans and external Mathlib cached context. Project import closure source/olean hashes and direct external module source/olean hashes bound before/after. Not a fresh transitive Mathlib build.';
  exit_code=$code; seconds=$elapsed; status=$(if($code -eq 0 -and $changed.Count -eq 0){'passed'}else{'excluded-failed-whole-module'});
  declaration_inventory=$decls; allowed_reads_before=$before; allowed_reads_after=$after; changed_context=$changed;
  stdout_sanitized=$sanitized
}
# Files are created by the caller with apply_patch, not by this read-only runner.
$receipt | ConvertTo-Json -Depth 12
