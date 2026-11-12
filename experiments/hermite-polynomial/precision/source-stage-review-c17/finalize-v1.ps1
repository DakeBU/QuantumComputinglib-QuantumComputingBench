$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskRel='experiments/hermite-polynomial/precision/source-stage-review-c17'
function Hash([string]$p){(Get-FileHash -LiteralPath (Join-Path $taskRoot $p) -Algorithm SHA256).Hash.ToLower()}
function Save([string]$name,$value){
  $taskPath=Join-Path $PSScriptRoot $name
  if(Test-Path -LiteralPath $taskPath){throw "Immutable output already exists: $name"}
  [System.IO.File]::WriteAllText($taskPath,($value|ConvertTo-Json -Depth 40)+"`n",[System.Text.UTF8Encoding]::new($false))
}
function Clean([string]$s){
  $s=$s.Replace($taskRoot,'<repo>').Replace($taskRoot.Replace('\','/'),'<repo>')
  [regex]::Replace($s,'[A-Za-z]:[\\/][^\r\n"''<>]*','<private-path>')
}
$taskVerified=@();$taskAxioms=[System.Collections.Generic.HashSet[string]]::new()
$taskRootPrints=[ordered]@{}
foreach($taskGroup in @('source','stage')){
  $taskReceiptPath="$taskRel/$taskGroup-replay-v3.json"
  $taskGate=Get-Content -LiteralPath (Join-Path $taskRoot $taskReceiptPath) -Raw|ConvertFrom-Json
  if($taskGate.exit_code -ne 0 -or -not $taskGate.bound_inputs_unchanged){throw 'Final replay not accepted'}
  $taskInputPath="$taskRel/$taskGroup-input-seal-v3.json"
  $taskInput=Get-Content -LiteralPath (Join-Path $taskRoot $taskInputPath) -Raw|ConvertFrom-Json
  if($taskInput.phase -ne 'BEFORE_ANY_GATE'){throw 'No preserved pre-gate window'}
  foreach($taskEntry in $taskGate.bindings_sha256.PSObject.Properties){
    if($taskEntry.Value -ne $taskInput.bindings_sha256.($taskEntry.Name) -or $taskEntry.Value -ne (Hash $taskEntry.Name)){
      throw "Bound input changed: $($taskEntry.Name)"
    }
  }
  foreach($taskEntry in $taskGate.private_olean_sha256.PSObject.Properties){
    if($taskEntry.Value -ne (Hash $taskEntry.Name)){throw 'Reviewer cache changed'}
  }
  $taskLeanCount=0;$taskPrintCount=0
  foreach($taskRow in $taskGate.execution){
    if($taskRow.exit_code -ne 0 -or $taskRow.log_sha256 -ne (Hash $taskRow.log)){throw 'Execution/log mismatch'}
    $taskText=Get-Content -LiteralPath (Join-Path $taskRoot $taskRow.log) -Raw
    if($taskText -match 'sorryAx|(?m): error:|declaration uses ''sorry'''){throw 'Rejected printed proof/error'}
    foreach($taskMatch in [regex]::Matches($taskText,"'([^']+)' depends on axioms: \[([^\]]*)\]")){
      $taskPrintCount++
      foreach($taskAx in ($taskMatch.Groups[2].Value -split ',')){
        $taskAx=$taskAx.Trim();if($taskAx){$null=$taskAxioms.Add($taskAx)}
      }
    }
    if($taskRow.command -match '^lake env lean '){$taskLeanCount++}
  }
  $taskRootPrints[$taskGroup]=$taskPrintCount
  $taskVerified+=@{group=$taskGroup;receipt=$taskReceiptPath;sha256=(Hash $taskReceiptPath);pre_gate_input_seal=$taskInputPath;pre_gate_seal_sha256=(Hash $taskInputPath);whole_lean_commands=$taskLeanCount;all_execution_exits=0;bindings_unchanged_now=$true;author_binding_checks=$taskGate.author_binding_checks.Count;private_cache_initially_absent=$taskGate.private_cache_initially_absent}
}
foreach($taskAx in $taskAxioms){if($taskAx -notin @('propext','Classical.choice','Quot.sound')){throw "Unexpected axiom: $taskAx"}}
$taskLeanPaths=@('NominalStageTransport.lean','ChronologicalTransport.lean','ConsumerChecks.lean')|ForEach-Object {'experiments/hermite-polynomial/precision/nominal-stage-transport/'+$_}
$taskLeanPaths+=@('PiecewiseSourceBudget.lean','PiecewiseConsumerChecks.lean')|ForEach-Object {'experiments/hermite-polynomial/precision/piecewise-source-budget/'+$_}
$taskLeanPaths+=@("$taskRel/SourceDiscriminatorsV1.lean","$taskRel/StageDiscriminatorsV1.lean")
foreach($taskP in $taskLeanPaths){
  $taskText=Get-Content -LiteralPath (Join-Path $taskRoot $taskP) -Raw
  if($taskText -match '\b(sorry|admit|native_decide|ofReduceBool)\b|(?m)^\s*(axiom|unsafe)\b'){throw "Forbidden new source construct: $taskP"}
}
$taskLocalBindings=[ordered]@{}
foreach($taskP in @("$taskRel/probe-seal-v2-additive.json","$taskRel/test_actual_local_v1.py","$taskRel/finalize-v1.ps1",'experiments/hermite-polynomial/precision/saved-action/saved_action.py')){$taskLocalBindings[$taskP]=Hash $taskP}
Save 'actual-local-input-seal-v1.json' @{phase='BEFORE_ACTUAL_LOCAL_TEST';bindings_sha256=$taskLocalBindings}
$taskPsi=[System.Diagnostics.ProcessStartInfo]::new()
$taskPsi.FileName=Join-Path $taskRoot '.venv/Scripts/python.exe';$taskPsi.WorkingDirectory=$taskRoot
$taskPsi.UseShellExecute=$false;$taskPsi.CreateNoWindow=$true;$taskPsi.RedirectStandardOutput=$true;$taskPsi.RedirectStandardError=$true
$taskPsi.Environment['PYTHONDONTWRITEBYTECODE']='1';$taskPsi.ArgumentList.Add("$taskRel/test_actual_local_v1.py");$taskPsi.ArgumentList.Add('-v')
$taskP=[System.Diagnostics.Process]::new();$taskP.StartInfo=$taskPsi;$null=$taskP.Start()
$taskOut=$taskP.StandardOutput.ReadToEndAsync();$taskErr=$taskP.StandardError.ReadToEndAsync()
if(-not $taskP.WaitForExit(120000)){$taskP.Kill($true);$taskP.WaitForExit()}
$taskLocalText=Clean ($taskOut.GetAwaiter().GetResult()+$taskErr.GetAwaiter().GetResult())
$taskLocalLog="$taskRel/actual-local-v1.log"
if(Test-Path -LiteralPath (Join-Path $taskRoot $taskLocalLog)){throw 'Local log immutable'}
[System.IO.File]::WriteAllText((Join-Path $taskRoot $taskLocalLog),$taskLocalText,[System.Text.UTF8Encoding]::new($false))
$taskLocalChanged=@($taskLocalBindings.Keys|Where-Object{$taskLocalBindings[$_] -ne (Hash $_)}).Count -ne 0
Save 'final-verification-v1.json' @{cycle=17;replays=$taskVerified;printed_root_counts=$taskRootPrints;axioms_union=@($taskAxioms);forbidden_source_scan='No forbidden construct in actual5 new author modules and2 own probe modules';actual_local=@{exit_code=$taskP.ExitCode;log=$taskLocalLog;log_sha256=(Hash $taskLocalLog);bindings_sha256=$taskLocalBindings;bindings_unchanged=(-not $taskLocalChanged)};earlier_runner_failures_retained=@('negative-evidence-v1.json','negative-evidence-v2.json','negative-evidence-v3-source-postprocess.json');public_logs_sanitized_before_write=$true;worker_tokens='unknown'}
if($taskP.ExitCode -ne 0 -or $taskLocalChanged){throw 'Actual local diagnostic failed; retained failed verification'}
$taskMath=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'mathematical-audit-v1.json') -Raw|ConvertFrom-Json
$taskArtifacts=[ordered]@{}
foreach($taskFile in Get-ChildItem -LiteralPath $PSScriptRoot -File){$taskPath="$taskRel/$($taskFile.Name)";$taskArtifacts[$taskPath]=Hash $taskPath}
Save 'independent-audit.json' @{cycle=17;reviewer='root/scalar_rounding_review_c15';status='ACCEPTED_NARROW_C_INTERNAL_PROVIDER_SCOPE';distinct_from_authors=$true;prior_cycles_disclosed=@(15,16);source_blind_publication_review=$false;mathematical_audit='mathematical-audit-v1.json';mathematical_audit_sha256=(Hash "$taskRel/mathematical-audit-v1.json");verification='final-verification-v1.json';verification_sha256=(Hash "$taskRel/final-verification-v1.json");fresh_own_replays=$taskVerified;own_kernel_roots=20;actual_local_test_methods=1;author_finite_test_methods=9;own_native_finite_discriminators=9;axioms_union=@($taskAxioms);artifact_sha256=$taskArtifacts;earlier_native_v1_v2='FAILED, retained; never relabeled. v2 pre-run window was not preserved, so v3 recompiled all selected sources under actual pre-gate seals.';original_signed_piL_target_preserved=$true;all_floor_Valid_error_produced_in_scope=$true;no_whole_transitive_compiler_rebuild=$true;parent_aggregate_gates_not_own=$true;remaining=$taskMath.remaining;scientific_ROOT=$false;public_SourceAnchor=$false;public_PURIFIED=$false;resource_winner=$false;worker_tokens='unknown';writes_stopped_after_handoff=$true}
Save 'handoff.json' @{cycle=17;reviewer='root/scalar_rounding_review_c15';scope='Only new source-stage-review-c17 subtree';status='SCOPED_REVIEW_COMPLETE_WRITES_STOPPED';audit='independent-audit.json';audit_sha256=(Hash "$taskRel/independent-audit.json");mathematical_audit_sha256=(Hash "$taskRel/mathematical-audit-v1.json");verification_sha256=(Hash "$taskRel/final-verification-v1.json");author_inputs=$taskMath.author_inputs;fresh_replays=$taskVerified;accepted='Original normalized target epsilon/2 from actual finite source/radius with produced floors; literal real full-word norm preservation and actual produced stage Valid plus chronological flatten product/apply growth bound';lineage=$taskMath.independence;rejected_claims=@('public SourceAnchor/PURIFIED/ROOT','complex PrimitiveSemantics adapter','old rank2k+6 inherited by finite source','global dense2^(np+a) attributed to actual local a+1 routine','surrogate contraction','scalar epsilon equals state error','finite/runtime/resource winner');failures_preserved=@('negative-evidence-v1.json','negative-evidence-v2.json','negative-evidence-v3-source-postprocess.json');remaining=$taskMath.remaining;no_author_production_task_history_registry_git_writes=$true;no_subagents=$true;writes_stopped=$true;worker_tokens='unknown'}
Write-Output "Audit SHA=$(Hash "$taskRel/independent-audit.json")"
Write-Output "Handoff SHA=$(Hash "$taskRel/handoff.json")"
Write-Output 'Writes stopped.'
