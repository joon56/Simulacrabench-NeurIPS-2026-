param([string]$Attempt='c6-01')
$ErrorActionPreference='Stop'
$watch=[Diagnostics.Stopwatch]::StartNew()
$d=$PSScriptRoot
$root=(Get-Location).Path
$entry=Get-Content -LiteralPath (Join-Path $d 'entry.json') -Encoding UTF8 -Raw | ConvertFrom-Json
$freeze=Get-Content -LiteralPath (Join-Path $d 'source-environment-freeze.json') -Encoding UTF8 -Raw | ConvertFrom-Json
$prior=@(Get-ChildItem -LiteralPath $d -Filter '*-process.json' -File)
$used=0.0
foreach($receipt in $prior){$used+=(Get-Content -LiteralPath $receipt.FullName -Encoding UTF8 -Raw | ConvertFrom-Json).supervisor_wall_seconds}
if($prior.Count -ge 3 -or (90-$used) -lt 30){throw 'Diagnostic allowance exhausted'}
if(([DateTimeOffset]::Parse($entry.work_cutoff_utc)-[DateTimeOffset]::UtcNow).TotalSeconds -lt 30){throw 'Closeout reserve reached'}
foreach($p in $prior){
 $r=Get-Content -LiteralPath $p.FullName -Encoding UTF8 -Raw | ConvertFrom-Json
 if($r.parser_reached -or $r.boundary_observation_unknown){throw 'Valid or unobservable C6 already consumed; no retry'}
}
foreach($property in $freeze.hashes.PSObject.Properties){
 $path=if([IO.Path]::IsPathRooted($property.Name)){$property.Name}else{Join-Path $root $property.Name}
 if((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $property.Value){throw ('Freeze mismatch: '+$property.Name)}
}
foreach($suffix in @('-start.json','-stdout.txt','-stderr.txt','-process.json','-samples.json')){
 if(Test-Path -LiteralPath (Join-Path $d ($Attempt+$suffix))){throw 'Attempt collision'}
}
$utf8=[Text.UTF8Encoding]::new($false)
function SaveJson($path,$value){[IO.File]::WriteAllText($path,($value | ConvertTo-Json -Depth 12),$utf8)}
SaveJson (Join-Path $d ($Attempt+'-start.json')) ([ordered]@{attempt=$Attempt;case='protobuf_graph';started_utc=[DateTimeOffset]::UtcNow.ToString('o');used=$used;remaining=90-$used;execution_stop_seconds=25;overall_cap_seconds=30;freeze_sha256=(Get-FileHash -LiteralPath (Join-Path $d 'source-environment-freeze.json')).Hash.ToLowerInvariant()})
$self=Get-Process -Id $PID
$self.ProcessorAffinity=[IntPtr]3
$env:OMP_NUM_THREADS='2';$env:MKL_NUM_THREADS='2';$env:OPENBLAS_NUM_THREADS='2';$env:CUDA_VISIBLE_DEVICES=''
$owned=@{}
$owned[$PID]=$self
$p=$null;$forced=$false;$reason='COMPLETE';$errorText=$null
$samples=New-Object 'System.Collections.Generic.List[object]'
$peakRss=0L;$peakPrivate=0L;$gap=0.0;$lastSample=0.0
function DiscoverOwned {
 $rows=@(Get-CimInstance Win32_Process -Property ProcessId,ParentProcessId,CreationDate,Name)
 do{
  $added=$false
  foreach($row in $rows){
   $id=[int]$row.ProcessId;$parent=[int]$row.ParentProcessId
   if($owned.ContainsKey($parent) -and -not $owned.ContainsKey($id)){
    $child=Get-Process -Id $id -ErrorAction SilentlyContinue
    if($child -and $child.StartTime -ge $self.StartTime){$null=$child.Handle;$null=$child.ProcessName;$owned[$id]=$child;$added=$true}
   }
  }
 }while($added)
}
try{
 DiscoverOwned
 if($owned.Count -ne 1){throw 'Unexpected existing supervisor child before launch'}
 $p=Start-Process -FilePath (Join-Path $root 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe') -ArgumentList @('-I','-X','faulthandler',('"'+(Join-Path $d 'check_boundary.py')+'"'),$Attempt,'protobuf_graph') -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $d ($Attempt+'-stdout.txt')) -RedirectStandardError (Join-Path $d ($Attempt+'-stderr.txt'))
 $null=$p.Handle;$null=$p.ProcessName;$owned[$p.Id]=$p
 do{
  DiscoverOwned
  $rss=0L;$private=0L;$live=@()
  foreach($process in $owned.Values){
   if(-not $process.HasExited){$process.Refresh();$rss+=$process.WorkingSet64;$private+=$process.PrivateMemorySize64;$live+=$process.Id}
  }
  $now=$watch.Elapsed.TotalSeconds
  if($lastSample -gt 0){$gap=[Math]::Max($gap,$now-$lastSample)}
  $lastSample=$now;$peakRss=[Math]::Max($peakRss,$rss);$peakPrivate=[Math]::Max($peakPrivate,$private)
  $samples.Add([ordered]@{seconds=$now;rss=$rss;private=$private;live_pids=$live})
  if($rss -ge 2147483648 -or $private -ge 2147483648){$reason='RESOURCE_LIMIT';$forced=$true;break}
  if($now -ge 25 -or [DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse($entry.work_cutoff_utc)){$reason='TIME_LIMIT';$forced=$true;break}
  if($p.HasExited){break}
  Start-Sleep -Milliseconds 40
 }while($true)
}catch{$errorText=$_.Exception.Message;$reason='OBSERVER_OR_ENTRY_ERROR';$forced=$true}
finally{
 if($forced){
  foreach($process in @($owned.Values | Where-Object {$_.Id -ne $PID} | Sort-Object StartTime -Descending)){
   if(-not $process.HasExited){$process.Kill()}
  }
 }
 foreach($process in @($owned.Values | Where-Object {$_.Id -ne $PID})){
  $remaining=[Math]::Max(0,[Math]::Min(5000,(30-$watch.Elapsed.TotalSeconds)*1000))
  if(-not $process.WaitForExit([int]$remaining)){$reason='UNREAPED_PROCESS'}
 }
}
$children=@(foreach($process in $owned.Values){if($process.Id -ne $PID){
 [ordered]@{pid=$process.Id;name=$process.ProcessName;has_exited=$process.HasExited;start_utc=$process.StartTime.ToUniversalTime().ToString('o');exit_code=$(if($process.HasExited){$process.ExitCode}else{$null})}
}})
$remainingPids=@($children | Where-Object {-not $_.has_exited} | ForEach-Object {$_.pid})
$pidPath=Join-Path $d ($Attempt+'-pid.json')
$actualPid=if(Test-Path -LiteralPath $pidPath){(Get-Content -LiteralPath $pidPath -Raw -Encoding UTF8 | ConvertFrom-Json).pid}else{$null}
$actual=@($children | Where-Object {$_.pid -eq $actualPid})
$tracePath=Join-Path $d ('attempts/'+$Attempt+'/trace.jsonl')
$events=@()
if(Test-Path -LiteralPath $tracePath){$events=@(Get-Content -LiteralPath $tracePath -Encoding UTF8 | ForEach-Object {$_ | ConvertFrom-Json})}
$parserReached=@($events | Where-Object {$_.event -eq 'protobuf_parser_enter'}).Count -eq 1
$parserReturned=@($events | Where-Object {$_.event -eq 'protobuf_graph_constructed_and_parsed'}).Count -eq 1
$assertPath=Join-Path $d ('attempts/'+$Attempt+'/check-result.json')
$assertions=if(Test-Path -LiteralPath $assertPath){Get-Content -LiteralPath $assertPath -Encoding UTF8 -Raw | ConvertFrom-Json}else{$null}
$blockedBuild=@($events | Where-Object {$_.event -in @('image_build_requested','sdk_image_build_chain','builder_function','project_mount','sandbox_create_started')}).Count
$stderrPath=Join-Path $d ($Attempt+'-stderr.txt')
$stderr=if(Test-Path -LiteralPath $stderrPath){Get-Content -LiteralPath $stderrPath -Raw -Encoding UTF8}else{''}
$elapsed=$watch.Elapsed.TotalSeconds
$outcome='INCONCLUSIVE'
if($forced -or $elapsed -gt 30 -or $used+$elapsed -gt 90 -or $remainingPids.Count -gt 0){$outcome=if($reason -match 'LIMIT|UNREAPED'){'LIMIT'}else{'INCONCLUSIVE'}}
elseif($blockedBuild){$outcome='BLOCKED_BOUNDARY'}
elseif($parserReturned -and $actual.Count -eq 1 -and $p.ExitCode -eq -1073741819 -and $actual[0].exit_code -eq -1073741819 -and $stderr -match 'access violation'){$outcome='SUFFICIENT_TRIGGER_REPRODUCED'}
elseif($parserReturned -and $assertions.assertions -eq 'PASS_EXIT_PENDING' -and $p.ExitCode -eq 0 -and $actual.Count -eq 1 -and $actual[0].exit_code -eq 0){$outcome='NOT_REPRODUCED'}
SaveJson (Join-Path $d ($Attempt+'-samples.json')) $samples
$receipt=[ordered]@{attempt=$Attempt;outcome=$outcome;reason=$reason;error=$errorText;supervisor_wall_seconds=$watch.Elapsed.TotalSeconds;aggregate_seconds=$used+$watch.Elapsed.TotalSeconds;cap_seconds=30;budget_seconds=90;forced=$forced;launcher_pid=$(if($p){$p.Id}else{$null});exit_code=$(if($p -and $p.HasExited){$p.ExitCode}else{$null});actual_python_pid=$actualPid;children=$children;remaining_owned_pids=$remainingPids;parser_reached=$parserReached;parser_returned=$parserReturned;boundary_observation_unknown=($reason -eq 'OBSERVER_OR_ENTRY_ERROR' -or $actual.Count -ne 1);assertions=$assertions;forbidden_build_events=$blockedBuild;peak_owned_tree_rss=$peakRss;peak_owned_tree_private=$peakPrivate;sample_count=$samples.Count;maximum_sample_gap_seconds=$gap;sampling_semantics='Current sampled working set/private sum of supervisor and discovered descendants; not continuous peak proof';cpu_affinity=3;gpu=0;remote_model=0;finished_utc=[DateTimeOffset]::UtcNow.ToString('o')}
SaveJson (Join-Path $d ($Attempt+'-process.json')) $receipt
$receipt | ConvertTo-Json -Depth 10
