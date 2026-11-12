$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$base = 'reviews/publication/constructive-tensor-train'
$private = "$base/decoder-c23-private"
$cache = "$base/decoder-c23-cache"
function Sha([string]$path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower() }
function Relative([string]$path) { $path.Substring($root.Length+1).Replace('\','/') }
function Sanitize([string]$value) {
  $clean = $value.Replace($root,'.').Replace($root.Replace('\','/'),'.')
  $clean = $clean -replace '(?s)Cannot convert value ".*?" to type "System.Int32"', 'Cannot convert value "<inherited LEAN_PATH redacted>" to type "System.Int32"'
  $clean = $clean -replace '[A-Za-z]:[\\/][^\r\n''" ]+', '[local-path-redacted]'
  $clean
}
$rawEvidence = @()
foreach ($file in (Get-ChildItem -LiteralPath $private -Filter '*-raw.log')) {
  $relativeRaw = Relative $file.FullName
  $suffix = $file.BaseName.Replace('-raw','')
  if ($suffix -eq 'target') { $suffix = 'initial-runner-native-warning' }
  $public = "$base/decoder-c23-$suffix.log"
  [IO.File]::WriteAllText((Join-Path $root $public),
    (Sanitize ([IO.File]::ReadAllText($file.FullName))),[Text.UTF8Encoding]::new($false))
  $stageReceipt = "$base/decoder-c23-$suffix-receipt.json"
  if (Test-Path -LiteralPath $stageReceipt) {
    $r = Get-Content -LiteralPath $stageReceipt -Raw | ConvertFrom-Json
    if ($r.public_sha256 -ne (Sha $public)) {
      $r | Add-Member -NotePropertyName original_public_derivative_sha256 -NotePropertyValue $r.public_sha256 -Force
      $r.public_sha256 = Sha $public
      $r | Add-Member -NotePropertyName derivative_sanitization -NotePropertyValue 'wrapped inherited LEAN_PATH value redacted; raw file unchanged' -Force
      [IO.File]::WriteAllText((Join-Path $root $stageReceipt),
        ($r | ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
    }
  }
  $rawEvidence += [ordered]@{raw=$relativeRaw;raw_sha256=Sha $relativeRaw;
    public_derivative=$public;public_sha256=Sha $public}
}
$packetPath = "$base/author-decoder-packet-v2.json"
$contextPath = "$base/author-formal-context.json"
$packet = Get-Content -LiteralPath $packetPath -Raw | ConvertFrom-Json
$original = Get-Content -LiteralPath "$base/author-decoder-packet.json" -Raw | ConvertFrom-Json
$packetDifferences = @()
foreach($property in $original.PSObject.Properties.Name) {
  if(($original.$property | ConvertTo-Json -Depth 12 -Compress) -ne
    ($packet.$property | ConvertTo-Json -Depth 12 -Compress)) { $packetDifferences += $property }
}
if($packetDifferences.Count -ne 1 -or $packetDifferences[0] -ne 'binding_sha256' -or
  @($original.PSObject.Properties).Count -ne @($packet.PSObject.Properties).Count) {
  throw 'Blind packet successor changed non-opaque fields'
}
$context = Get-Content -LiteralPath $contextPath -Raw | ConvertFrom-Json
if((Sha $packet.module) -ne $packet.module_sha256 -or
  (Sha 'lean-toolchain') -ne $packet.toolchain_sha256 -or
  (Sha 'lake-manifest.json') -ne $packet.manifest_sha256 -or
  (Sha 'lakefile.lean') -ne $packet.lakefile_sha256 -or
  (Sha $contextPath) -ne $packet.formal_context_sha256) {
  throw 'Formal input changed from blind packet binding'
}
foreach($file in $context.files) {
  if((Sha $file.path) -ne $file.sha256) { throw "Formal provider source changed: $($file.path)" }
}
$fullRead = @('AGENTS.md','HARNESS.md','.agents/skills/qbe-substantive-worker/SKILL.md',
  'docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md',
  'docs/evidence-routed-memory-protocol.md','lean-toolchain','lakefile.lean','lake-manifest.json')
$fullRead += @($context.files.path)
$contextBindings = @()
foreach($path in $fullRead) {
  $contextBindings += [ordered]@{path=$path;sha256=Sha $path;consulted='complete source text'}
}
$contextBindings += [ordered]@{path=$packetPath;sha256=Sha $packetPath;consulted='complete packet'}
$contextBindings += [ordered]@{path="$base/author-decoder-packet.json";sha256=Sha "$base/author-decoder-packet.json";consulted='original v1 complete packet; superseded only in opaque binding'}
$contextBindings += [ordered]@{path=$contextPath;sha256=Sha $contextPath;
  consulted='metadata and source snapshots; initial combined output truncated; complete actual matching source files subsequently read'}
$contextBindings += [ordered]@{path='QuantumBlockEncoding/SelectedRyPlane.lean';
  sha256=Sha 'QuantumBlockEncoding/SelectedRyPlane.lean';consulted='first 12 lines: import and header only'}
$contextBindings += [ordered]@{path='.lake/packages/mathlib/Mathlib/Logic/Equiv/Fin/Basic.lean';
  sha256=Sha '.lake/packages/mathlib/Mathlib/Logic/Equiv/Fin/Basic.lean';consulted='finProdFinEquiv definition region only'}
$freshModules = @('RealAmplitudePreparation','SequentialBondPreparation','ThinLQ',
  'TensorTrainCanonical','AdjacentGivens','RectangularGivens','ConstructiveThinLQ',
  'ConstructiveTensorTrain')
$sourceAndOlean = @()
foreach($module in $freshModules) {
  $source = "QuantumBlockEncoding/$module.lean"
  $output = "$cache/QuantumBlockEncoding/$module.olean"
  $sourceAndOlean += [ordered]@{source=$source;source_sha256=Sha $source;
    produced_olean=$output;olean_sha256=Sha $output}
}
$stages = @()
foreach($file in (Get-ChildItem -LiteralPath $base -Filter 'decoder-c23-*-receipt.json')) {
  $r = Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json
  $stages += [ordered]@{path=Relative $file.FullName;sha256=Sha $file.FullName;receipt=$r}
}
$checksLog = Get-Content -LiteralPath "$base/decoder-c23-checks-attempt2.log" -Raw
$axioms = @()
foreach($decl in $packet.declarations) {
  $escaped = [Regex]::Escape($decl)
  $match = [Regex]::Match($checksLog, "'$escaped' (does not depend on any axioms|depends on axioms:\s*\[[^\]]*\])")
  $axioms += [ordered]@{declaration=$decl;printed_axiom_evidence=if($match.Success){$match.Value}else{'MISSING'}}
}
$artifacts = @()
foreach($file in (Get-ChildItem -LiteralPath $base -Filter 'decoder-c23-*' -File)) {
  if($file.Name -eq 'decoder-c23-freeze.json') { continue }
  $text = [IO.File]::ReadAllText($file.FullName)
  if($text -match '(?i)(?<![A-Za-z])[A-Z]:[\\/]') {
    throw "Public local-path leakage in $($file.Name)"
  }
  $artifacts += [ordered]@{path=Relative $file.FullName;sha256=Sha $file.FullName;bytes=$file.Length}
}
$final = [ordered]@{
  schema_version=1;role='source-blind-formal-decoder';decoder_identity='/root/ctt_source_blind_decoder_c23';
  direction_fingerprint='CTT_FORMAL_TO_MATH_WHOLE_MODULE';
  expected_information_gain='detect hidden premise, basis/index, rank meaning and terminal-sector drift';
  status='BOUNDED_WHOLE_MODULE_DECODER_FROZEN';frozen_at_utc=[DateTime]::UtcNow.ToString('o');
  binding_sha256=$packet.binding_sha256;opaque_binding_recomputed=$false;
  packet_v1_path="$base/author-decoder-packet.json";packet_v1_sha256=Sha "$base/author-decoder-packet.json";
  packet_transition='v2 compared mechanically with v1; only binding_sha256 changed; all formal source/context/toolchain/manifest bytes unchanged';
  mechanically_observed_packet_differences=$packetDifferences;
  packet_path=$packetPath;packet_sha256=Sha $packetPath;
  formal_context_path=$contextPath;formal_context_sha256=Sha $contextPath;
  target_path=$packet.module;target_sha256=Sha $packet.module;
  toolchain=(Get-Content -LiteralPath 'lean-toolchain' -Raw).Trim();
  lean_version=((& lean --version | Out-String).Trim());
  public_declarations=$packet.declarations;reconstructed_inventory_count=$packet.declarations.Count;
  actual_checked_signatures="$base/decoder-c23-checks-attempt2.log";axiom_census=$axioms;
  independent_symbolic_consumer="$base/decoder-c23-consumer.lean";
  independent_consumer_log="$base/decoder-c23-consumer-attempt2.log";
  human_reconstruction="$base/decoder-c23-reconstruction.txt";
  formal_logical_premises=@('boundary_normalized: chainMass C v = 1',
    'stateBoundary_normalized: sum x:Word n, (contract C x 0 0)^2 = 1');
  output_proof_fields=@('CoreFactorization.factorization','CoreFactorization.orthogonal',
    'Result.rightCanonical','Result.rankReduced','Result.action');
  mathematical_boundaries=@('real exact amplitudes only','all terminal labels included in general mass',
    'backward min dimensions, not algebraic tensor rank','no physical-wire/flat-basis bridge in target',
    'no primitive circuit/completion/gate-cost/storage/runtime/finite-bit certificate');
  direct_target_source_compiled=$true;cached_target_used_as_source_standin=$false;
  fresh_bounded_sources=$sourceAndOlean;remaining_provider_boundary='Mathlib, standard library and project imports outside these eight modules use inherited caches copied only into owned cache where namespace resolution requires it';
  provider_inventory="$base/decoder-c23-provider-inventory-consumer-attempt2.json";
  whole_mathlib_rebuilt=$false;full_repository_lean_and_tests_gate='NOT_RUN: focused decoder scope; no mutation of existing caches authorized';
  documentation_gate='NOT_RUN: no production or reader-site edits';
  inherited_verso_warning='Lake environment discovery warned about existing local verso changes; not altered by decoder';
  contexts_consulted=$contextBindings;import_headers_additional_context='exact traversed local import headers and hashes are in the bound provider inventory';
  environment_context=@('dispatch and host filesystem context','tool command availability',
    'native Lean version/help/print-libdir','lake env lean version and LEAN_PATH discovery',
    'optional wsl --list --quiet returned nonzero with garbled UTF-16 display; WSL not used',
    'owned compilation process diagnostics and private-cache directory metadata');
  withheld_context_read=$false;withheld_exclusions=$packet.withheld;
  source_agreement_verdict=$null;publication_acceptance_verdict=$null;
  process_memory_ids=@();single_route=$true;subagents_spawned=0;
  production_or_registry_edits=$false;git_edits=$false;existing_cache_mutated=$false;
  failed_attempts=@(
    [ordered]@{attempt='initial target runner';failure_class='IMPLEMENTATION_FAILED';
      detail='PowerShell native stderr terminated on existing verso warning; raw retained'},
    [ordered]@{attempt='providers attempt 1';failure_class='IMPLEMENTATION_FAILED';
      detail='private LEAN_PATH setup lost quoting; seven source calls completed but not claimed as final overlay evidence'},
    [ordered]@{attempt='providers attempt 2';failure_class='ENV_BLOCKED';detail='encoded nested PowerShell blocked by host policy: 786'},
    [ordered]@{attempt='providers attempt 3';failure_class='ENV_BLOCKED';
      detail='Lean resolves first namespace directory without per-file fallback: UniformlyControlledRy private olean missing'},
    [ordered]@{attempt='checks attempt 1';failure_class='IMPLEMENTATION_FAILED';
      detail='unknown pp.width option; all type/axiom output retained but not claimed as passing check stage'},
    [ordered]@{attempt='consumer attempt 1';failure_class='IMPLEMENTATION_FAILED';
      detail='three nil-cardinality simplification goals unresolved; failed elaboration printed sorryAx in those three auxiliary proofs; never accepted'});
  salvage='raw wrapper/environment failures retained; no mathematical route refuted or fragment promoted';
  purification_or_exposition_seal='NOT_CLAIMED; distinct source-first comparison required';
  raw_evidence=$rawEvidence;stage_receipts=$stages;public_artifacts=$artifacts;
  public_local_machine_path_scan='PASS';raw_logs_are_private_and_may_contain_local_paths=$true
}
foreach($name in @('providers-attempt4','target-fresh-attempt1','checks-attempt2','consumer-attempt2')) {
  $r = Get-Content -LiteralPath "$base/decoder-c23-$name-receipt.json" -Raw | ConvertFrom-Json
  if($r.exit_code -ne 0) { throw "Required final stage $name failed" }
}
if($axioms.printed_axiom_evidence -contains 'MISSING') { throw 'Missing declaration axiom evidence' }
if($checksLog -match 'sorryAx') { throw 'Placeholder axiom in accepted target census' }
$acceptedConsumer = Get-Content -LiteralPath "$base/decoder-c23-consumer-attempt2.log" -Raw
if($acceptedConsumer -match 'sorryAx') { throw 'Placeholder axiom in accepted consumer' }
[IO.File]::WriteAllText((Join-Path $root "$base/decoder-c23-freeze.json"),
  ($final | ConvertTo-Json -Depth 20)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output ([ordered]@{path="$base/decoder-c23-freeze.json";sha256=Sha "$base/decoder-c23-freeze.json";
  reconstruction_sha256=Sha "$base/decoder-c23-reconstruction.txt"} | ConvertTo-Json)
