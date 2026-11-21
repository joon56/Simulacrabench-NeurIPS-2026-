param([ValidateSet('probe','boundary','baseline','fixed','isolate-empty','isolate-fixed')][string]$Mode)
$ErrorActionPreference='Stop'
$root=Split-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) -Parent
$temp=Join-Path $root 'tmp/a040-local-preparation-repair2'
$python=Join-Path $root 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe'
$deadline=[DateTimeOffset]::Parse('2026-10-05T09:53:15Z')
if([DateTimeOffset]::UtcNow.AddSeconds(30) -ge $deadline){throw 'Execution cutoff; reserve closeout'}
$prior=@(Get-ChildItem -LiteralPath $PSScriptRoot -Filter 'process-*.json' | ForEach-Object {Get-Content -Encoding UTF8 $_.FullName -Raw|ConvertFrom-Json})
$used=($prior|Measure-Object -Property wall_seconds -Sum).Sum
if($used+30 -gt 180){throw 'Aggregate process budget exhausted'}
$number=$prior.Count+1
$prefix=Join-Path $PSScriptRoot ('process-'+$number)
$gate=Join-Path $temp ('gate-'+$number)
if(Test-Path ($prefix+'.json')){throw 'Record collision'}
$script=if($Mode -eq 'probe'){'probe.py'}elseif($Mode.StartsWith('isolate-')){'isolate.py'}else{'check_local.py'}
$snapshot=Join-Path $temp ('source-'+$number)
New-Item -ItemType Directory $snapshot | Out-Null
foreach($name in @('run_check.ps1',$script,'local_guard.py')){if(Test-Path (Join-Path $PSScriptRoot $name)){Copy-Item (Join-Path $PSScriptRoot $name) $snapshot}}
$watch=[Diagnostics.Stopwatch]::StartNew()
$failure=$null
$pidOwned=$null
$exitCode=$null
$affinity=$null
try{
 $p=Start-Process -FilePath $python -ArgumentList @('-I','-S','-B','-X','utf8',('"'+$PSScriptRoot+'/'+$script+'"'),$Mode,('"'+$gate+'"'),$number) -WorkingDirectory $temp -WindowStyle Hidden -PassThru -RedirectStandardOutput ($prefix+'-stdout.txt') -RedirectStandardError ($prefix+'-stderr.txt')
 $handle=$p.Handle
 $pidOwned=$p.Id
 if(!$p.HasExited){
  $available=$p.ProcessorAffinity.ToInt64()
  $mask=[long]0
  $count=0
  for($bit=0;$bit -lt 63 -and $count -lt 2;$bit++){ $value=([long]1 -shl $bit);if(($available -band $value) -ne 0){$mask=$mask -bor $value;$count++} }
  $p.ProcessorAffinity=[IntPtr]$mask
  $affinity=$p.ProcessorAffinity.ToInt64()
  [IO.File]::WriteAllText($gate,'CPU affinity set')
 }
 if(!$p.WaitForExit(27000)){taskkill /PID $pidOwned /T /F | Out-Null;throw 'Owned process timeout'}
 $p.WaitForExit()
 $exitCode=$p.ExitCode
}catch{$failure=$_.ToString()}
$residual=if($pidOwned){@(Get-Process -Id $pidOwned -ErrorAction SilentlyContinue).Count}else{0}
@{mode=$Mode;number=$number;pid=$pidOwned;exit_code=$exitCode;wall_seconds=$watch.Elapsed.TotalSeconds;error=$failure;affinity_mask=$affinity;owned_pid_remaining=$residual;hidden=$true;timeout_seconds=27} | ConvertTo-Json | Set-Content -Encoding UTF8 ($prefix+'.json')
Get-Content -Encoding UTF8 ($prefix+'-stdout.txt') -ErrorAction SilentlyContinue
Get-Content -Encoding UTF8 ($prefix+'-stderr.txt') -ErrorAction SilentlyContinue
if($failure -or $exitCode -ne 0 -or $residual){exit 1}
