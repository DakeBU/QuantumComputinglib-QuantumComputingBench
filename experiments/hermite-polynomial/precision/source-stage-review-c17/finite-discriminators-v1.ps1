$ErrorActionPreference='Stop'
function Assert([bool]$condition,[string]$label){if(-not $condition){throw "IMPLEMENTATION_FAILED: $label"};Write-Output "PASS $label"}
function CX([int]$i,[int]$c,[int]$t){
  $taskBits=@();for($taskQ=0;$taskQ -lt 4;$taskQ++){$taskBits+=([int][Math]::Floor($i/[Math]::Pow(2,$taskQ))%2)}
  if($taskBits[$c] -eq 1){$taskBits[$t]=1-$taskBits[$t]}
  $taskResult=0;for($taskQ=0;$taskQ -lt 4;$taskQ++){$taskResult+=$taskBits[$taskQ]*[int][Math]::Pow(2,$taskQ)}
  $taskResult
}
Assert ((CX (CX 1 0 1) 1 2) -eq 7 -and (CX (CX 1 1 2) 0 1) -eq 3) 'independent tuple-bit noncommuting CX chronology'
Assert ((CX 9 0 2) -eq 13 -and (CX 9 2 0) -eq 9) 'q0 LSB control direction and high spectator retained'
$taskX=@(2.0,-3.0,5.0,7.0,-11.0,13.0,-17.0,19.0)
$taskBefore=0.0;foreach($taskV in $taskX){$taskBefore+=$taskV*$taskV}
$taskC=[Math]::Cos(-1.4/2);$taskS=[Math]::Sin(-1.4/2)
$taskY=@($taskX)
for($taskI=0;$taskI -lt 8;$taskI+=2){$taskY[$taskI]=$taskC*$taskX[$taskI]-$taskS*$taskX[$taskI+1];$taskY[$taskI+1]=$taskS*$taskX[$taskI]+$taskC*$taskX[$taskI+1]}
$taskAfter=0.0;foreach($taskV in $taskY){$taskAfter+=$taskV*$taskV}
Assert ([Math]::Abs($taskBefore-$taskAfter) -lt 1e-10) 'finite full real-vector norm diagnostic, no projection'
Assert ((1.0+1.0/3)*(1.0+1.0/4)-1 -gt 1.0/3+1.0/4) 'multiplicative error exceeds additive sum'
Assert ((1*1+1*1) -eq 2) 'surrogate [[1,-1],[1,1]] has Gram2I, no surrogate contraction'
Assert ([Math]::Sqrt(4.0) -eq 2.0 -and 2.0 -gt 1.0) 'coordinate radius1 is not full vector error1'
Assert ([Math]::Pow(4,2+1) -eq 64 -and [Math]::Pow(4,12+2) -gt 64) 'local a+1 stage carrier is not automatic np+a carrier'
Assert ((4*3*3+2*3+1) -eq 43 -and 43 -gt 2*0+6) 'precision-dependent tail degree cannot inherit old k-only rank'
Assert (-1.0 -ne 1.0) 'signed normalized target is not a phase quotient'
Write-Output 'Nine finite discriminators; diagnostics only, no runtime or ROOT certificate.'
