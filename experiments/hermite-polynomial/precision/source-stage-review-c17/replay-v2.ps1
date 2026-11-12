param([ValidateSet('source','stage')][string]$Group)
$ErrorActionPreference='Stop'
$taskRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$taskRel='experiments/hermite-polynomial/precision/source-stage-review-c17'
$taskPrefix='experiments/hermite-polynomial/precision/'
$taskReceipt=Join-Path $PSScriptRoot "$Group-replay-v2.json"
if(Test-Path -LiteralPath $taskReceipt){throw 'Refusing immutable receipt overwrite'}
$taskCache=Join-Path $PSScriptRoot ".cache/$Group-v2"
if(Test-Path -LiteralPath $taskCache){throw 'Fresh cache required'}
New-Item -ItemType Directory -Path "$taskCache/QuantumBlockEncoding" -Force|Out-Null
function Hash([string]$p){(Get-FileHash -LiteralPath (Join-Path $taskRoot $p) -Algorithm SHA256).Hash.ToLower()}
function Clean([string]$s){
  $s=$s.Replace($taskRoot,'<repo>').Replace($taskRoot.Replace('\','/'),'<repo>')
  [regex]::Replace($s,'[A-Za-z]:[\\/][^\r\n"''<>]*','<private-path>')
}
$taskSourceModules=@(
  @('QuantumBlockEncoding/HermitePolynomial.lean','QuantumBlockEncoding/HermitePolynomial'),
  @('QuantumBlockEncoding/HermiteBernstein.lean','QuantumBlockEncoding/HermiteBernstein'),
  @('QuantumBlockEncoding/StoredHermiteCoefficients.lean','QuantumBlockEncoding/StoredHermiteCoefficients'),
  @('QuantumBlockEncoding/HermiteStatePreparation.lean','QuantumBlockEncoding/HermiteStatePreparation'),
  @('QuantumBlockEncoding/HermiteIntervalMass.lean','QuantumBlockEncoding/HermiteIntervalMass'),
  @(($taskPrefix+'coefficient-range/CoefficientRange.lean'),'CoefficientRange'),
  @(($taskPrefix+'finite-exp/FiniteExp.lean'),'FiniteExp'),
  @(($taskPrefix+'finite-exp-degree/FiniteExpDegree.lean'),'FiniteExpDegree'),
  @(($taskPrefix+'finite-middle-source/FiniteMiddleSource.lean'),'FiniteMiddleSource'),
  @(($taskPrefix+'finite-middle-source/ConsumerChecks.lean'),'ConsumerChecks'),
  @(($taskPrefix+'NormalizationStability.lean'),'NormalizationStability'),
  @(($taskPrefix+'radius-supplier/RadiusSupplier.lean'),'RadiusSupplier'),
  @(($taskPrefix+'radius-stability/RadiusStability.lean'),'RadiusStability'),
  @(($taskPrefix+'global-radius-budget/GlobalRadiusBudget.lean'),'GlobalRadiusBudget'),
  @(($taskPrefix+'piecewise-source-budget/PiecewiseSourceBudget.lean'),'PiecewiseSourceBudget'),
  @(($taskPrefix+'piecewise-source-budget/PiecewiseConsumerChecks.lean'),'PiecewiseConsumerChecks'),
  @(($taskRel+'/SourceDiscriminatorsV1.lean'),'SourceDiscriminatorsV1')
)
$taskStageModules=@(
  @(($taskPrefix+'finite-trig/FiniteTrig.lean'),'FiniteTrig'),
  @(($taskPrefix+'saved-rounding/SavedRounding.lean'),'SavedRounding'),
  @(($taskPrefix+'saved-stage-interpreter/SavedStageInterpreter.lean'),'SavedStageInterpreter'),
  @(($taskPrefix+'saved-stage-interpreter/StageOperatorBound.lean'),'StageOperatorBound'),
  @(($taskPrefix+'nonunitary-transport/NonunitaryTransport.lean'),'NonunitaryTransport'),
  @(($taskPrefix+'nominal-stage-transport/NominalStageTransport.lean'),'NominalStageTransport'),
  @(($taskPrefix+'nominal-stage-transport/ChronologicalTransport.lean'),'ChronologicalTransport'),
  @(($taskPrefix+'nominal-stage-transport/ConsumerChecks.lean'),'ConsumerChecks'),
  @(($taskRel+'/StageDiscriminatorsV1.lean'),'StageDiscriminatorsV1')
)
$taskBefore=[ordered]@{}
$taskBindingChecks=@()
foreach($taskAuthor in @('nominal-stage-transport','piecewise-source-budget')){
  $taskFolder=$taskPrefix+$taskAuthor
  foreach($taskFile in Get-ChildItem -LiteralPath (Join-Path $taskRoot $taskFolder) -File){
    $taskP=$taskFolder+'/'+$taskFile.Name; $taskBefore[$taskP]=Hash $taskP
  }
  $taskResultName=if($taskAuthor -eq 'nominal-stage-transport'){'result-v1.json'}else{'result.json'}
  $taskResult=Get-Content -LiteralPath (Join-Path $taskRoot "$taskFolder/$taskResultName") -Raw|ConvertFrom-Json
  foreach($taskMapName in @('bindings_sha256','dependency_hashes','artifact_hashes')){
    if($null -eq $taskResult.$taskMapName){continue}
    foreach($taskEntry in $taskResult.$taskMapName.PSObject.Properties){
      $taskP=if($taskMapName -eq 'artifact_hashes'){"$taskFolder/$($taskEntry.Name)"}else{$taskEntry.Name}
      $taskActual=Hash $taskP; $taskBefore[$taskP]=$taskActual
      $taskBindingChecks+=@{path=$taskP;expected=$taskEntry.Value;actual=$taskActual;matches=($taskEntry.Value -eq $taskActual)}
    }
  }
}
foreach($taskP in @('lean-toolchain','lake-manifest.json','AGENTS.md','HARNESS.md',
  '.agents/skills/qbe-substantive-worker/SKILL.md','docs/theorem-publication-protocol.md',
  'docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md','reports/process-memory.json',
  'experiments/hermite-polynomial/precision/saved-action/saved_action.py',
  "$taskRel/.gitignore","$taskRel/probe-seal-v1.json","$taskRel/replay-v2.ps1", "$taskRel/finite-discriminators-v1.ps1")){
  $taskBefore[$taskP]=Hash $taskP
}
foreach($taskM in ($taskSourceModules+$taskStageModules)){$taskBefore[$taskM[0]]=Hash $taskM[0]}
$taskRows=@(); $taskExit=0; $taskClass='NONE'
if(@($taskBindingChecks|Where-Object {-not $_.matches}).Count){$taskExit=1;$taskClass='SOURCE_INVALID_BINDING';}
else{
  $taskModules=if($Group -eq 'source'){$taskSourceModules}else{$taskStageModules}
  $taskCommands=@()
  foreach($taskM in $taskModules){$taskCommands+=,@('lake','env','lean','-o',"$taskRel/.cache/$Group-v2/$($taskM[1]).olean",$taskM[0])}
  $taskTest=if($Group -eq 'source'){'piecewise-source-budget/test_piecewise_source.py'}else{'nominal-stage-transport/test_discriminators.py'}
  $taskCommands+=,@('.venv/Scripts/python.exe',($taskPrefix+$taskTest),'-v')
  if($Group -eq 'stage'){$taskCommands+=,@((Get-Command pwsh).Source,'-NoProfile','-File',"$taskRel/finite-discriminators-v1.ps1")}
  for($taskI=0;$taskI -lt $taskCommands.Count;$taskI++){
    $taskCmd=$taskCommands[$taskI]
    $taskPsi=[System.Diagnostics.ProcessStartInfo]::new()
    $taskPsi.FileName=if($taskCmd[0] -eq 'lake'){(Get-Command lake).Source}else{$taskCmd[0]}
    $taskPsi.WorkingDirectory=$taskRoot; $taskPsi.UseShellExecute=$false
    $taskPsi.CreateNoWindow=$true; $taskPsi.RedirectStandardOutput=$true; $taskPsi.RedirectStandardError=$true
    $taskPsi.Environment['LEAN_PATH']=$taskCache
    $taskPsi.Environment['PYTHONDONTWRITEBYTECODE']='1'
    foreach($taskA in $taskCmd[1..($taskCmd.Count-1)]){$taskPsi.ArgumentList.Add($taskA)}
    $taskP=[System.Diagnostics.Process]::new();$taskP.StartInfo=$taskPsi
    $taskWatch=[System.Diagnostics.Stopwatch]::StartNew()
    $null=$taskP.Start();$taskOut=$taskP.StandardOutput.ReadToEndAsync();$taskErr=$taskP.StandardError.ReadToEndAsync()
    if(-not $taskP.WaitForExit(240000)){$taskP.Kill($true);$taskP.WaitForExit();$taskClass='ENV_BLOCKED_TIMEOUT'}
    $taskText=Clean ($taskOut.GetAwaiter().GetResult()+$taskErr.GetAwaiter().GetResult())
    $taskExit=$taskP.ExitCode
    $taskLog="$taskRel/$Group-replay-v2-$taskI.log"
    if(Test-Path -LiteralPath (Join-Path $taskRoot $taskLog)){throw 'Refusing log overwrite'}
    [System.IO.File]::WriteAllText((Join-Path $taskRoot $taskLog),$taskText,[System.Text.UTF8Encoding]::new($false))
    $taskRows+=@{command=(Clean ($taskCmd -join ' '));exit_code=$taskExit;seconds=$taskWatch.Elapsed.TotalSeconds;log=$taskLog;log_sha256=(Hash $taskLog)}
    Write-Output "$Group gate $taskI exit=$taskExit"
    if($taskExit -ne 0){if($taskClass -eq 'NONE'){$taskClass='IMPLEMENTATION_FAILED'};Write-Output $taskText;break}
  }
}
$taskAfter=[ordered]@{};foreach($taskP in $taskBefore.Keys){$taskAfter[$taskP]=Hash $taskP}
$taskUnchanged=@($taskBefore.Keys|Where-Object {$taskBefore[$_] -ne $taskAfter[$_]}).Count -eq 0
$taskOleans=[ordered]@{};foreach($taskFile in Get-ChildItem -LiteralPath $taskCache -Filter '*.olean' -Recurse){
  $taskP=$taskRel+'/.cache/'+$Group+'-v1/'+[System.IO.Path]::GetRelativePath($taskCache,$taskFile.FullName).Replace('\','/')
  $taskOleans[$taskP]=Hash $taskP
}
$taskObject=[ordered]@{cycle=17;reviewer='root/scalar_rounding_review_c15';group=$Group;exit_code=$taskExit;failure_class=$taskClass;full_selected_sources=$true;private_cache_initially_absent=$true;author_cache_used=$false;transitive_substrate='Other pinned production/Mathlib packages reused; not a compiler/all-transitive rebuild';native_runner='PowerShell7/System.Diagnostics.Process; sanitized before writes';bindings_sha256=$taskBefore;bound_inputs_unchanged=$taskUnchanged;author_binding_checks=$taskBindingChecks;execution=$taskRows;private_olean_sha256=$taskOleans;scientific_ROOT=$false;public_SourceAnchor=$false;public_PURIFIED=$false;worker_tokens='unknown'}
[System.IO.File]::WriteAllText($taskReceipt,($taskObject|ConvertTo-Json -Depth 30)+"`n",[System.Text.UTF8Encoding]::new($false))
Write-Output "Receipt $taskRel/$Group-replay-v2.json SHA=$((Get-FileHash -LiteralPath $taskReceipt).Hash.ToLower())"
exit $taskExit
