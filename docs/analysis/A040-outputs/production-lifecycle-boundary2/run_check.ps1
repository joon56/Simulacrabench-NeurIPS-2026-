param([Parameter(Mandatory=$true)][string]$Attempt,[Parameter(Mandatory=$true)][ValidateSet('success','builder_fail','stall')][string]$Case)
$ErrorActionPreference='Stop'
$d=$PSScriptRoot
$root=(Get-Location).Path
$entry=Get-Content -LiteralPath (Join-Path $d 'entry.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$used=0.0
Get-ChildItem -LiteralPath $d -Filter '*-process.json' -File | ForEach-Object {
    $used+=(Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8 | ConvertFrom-Json).supervisor_wall_seconds
}
$cap=if($Case -eq 'stall'){210}else{60}
$kill=if($Case -eq 'stall'){200}else{50}
if ((420-$used) -lt $cap) {throw 'Aggregate check budget cannot cover worst case'}
if (([DateTimeOffset]::Parse($entry.work_cutoff_utc)-[DateTimeOffset]::UtcNow).TotalSeconds -lt $cap) {throw 'Closeout reserve would be consumed'}
foreach($suffix in @('-stdout.txt','-stderr.txt','-process.json','-preflight.json')) {
    if(Test-Path -LiteralPath (Join-Path $d ($Attempt+$suffix))){throw 'Attempt output collision'}
}
$manifest=Get-Content -LiteralPath (Join-Path $d 'source-manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($row in $manifest.files){if((Get-FileHash -LiteralPath (Join-Path $d $row.path)).Hash.ToLower() -ne $row.sha256){throw ('Source freeze mismatch '+$row.path)}}
$inputs=@(foreach($name in @('source-manifest.json','boundary_transport.py','fixture_transport.py','local_guard.py','check_boundary.py','run_check.ps1')){@{path=$name;sha256=(Get-FileHash -LiteralPath (Join-Path $d $name)).Hash.ToLower()}})
@{attempt=$Attempt;case=$Case;start_utc=[DateTimeOffset]::UtcNow.ToString('o');used_seconds=$used;remaining_seconds=420-$used;cap_seconds=$cap;kill_seconds=$kill;inputs=$inputs} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $d ($Attempt+'-preflight.json')) -Encoding UTF8
$watch=[Diagnostics.Stopwatch]::StartNew()
$p=Start-Process -FilePath (Join-Path $root 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe') -ArgumentList @('-I','-X','faulthandler',('"'+(Join-Path $d 'check_boundary.py')+'"'),$Attempt,$Case) -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $d ($Attempt+'-stdout.txt')) -RedirectStandardError (Join-Path $d ($Attempt+'-stderr.txt'))
$ownedHandle=$p.Handle
$p.ProcessorAffinity=[IntPtr]3
$childStart=$p.StartTime.ToUniversalTime().ToString('o')
$forced=$false
$actualPython=$null
$tracePath=Join-Path $d ('attempts/'+$Attempt+'/trace.jsonl')
while(-not $p.WaitForExit(500)){
    if($null -eq $actualPython -and (Test-Path -LiteralPath $tracePath)){
        $first=Get-Content -LiteralPath $tracePath -Encoding UTF8 -TotalCount 1 | ConvertFrom-Json
        if($first.pid){
            $actualPython=Get-Process -Id $first.pid -ErrorAction SilentlyContinue
            if($actualPython){$actualHandle=$actualPython.Handle;$actualPython.ProcessorAffinity=[IntPtr]3}
        }
    }
    if($watch.Elapsed.TotalSeconds -ge $kill){
        $forced=$true
        if($actualPython -and -not $actualPython.HasExited){Stop-Process -Id $actualPython.Id}
        if(-not $p.HasExited){Stop-Process -Id $p.Id}
        break
    }
}
if(-not $p.WaitForExit(9000)){throw ('Owned process not reaped: '+$p.Id)}
$exitCode=$p.ExitCode
$childExit=$p.ExitTime.ToUniversalTime().ToString('o')
$childWall=($p.ExitTime-$p.StartTime).TotalSeconds
$watch.Stop()
$receipt=@{attempt=$Attempt;case=$Case;pid=$p.Id;child_start_utc=$childStart;child_exit_utc=$childExit;child_wall_seconds=$childWall;supervisor_wall_seconds=$watch.Elapsed.TotalSeconds;exit_code=$exitCode;forced=$forced;remaining_owned_pid=0;cpu_affinity=3;aggregate_seconds=$used+$watch.Elapsed.TotalSeconds;cap_seconds=$cap;within_cap=($watch.Elapsed.TotalSeconds -le $cap)}
if($actualPython){
    $receipt.actual_python=@{pid=$actualPython.Id;start_utc=$actualPython.StartTime.ToUniversalTime().ToString('o');exit_utc=$actualPython.ExitTime.ToUniversalTime().ToString('o');wall_seconds=($actualPython.ExitTime-$actualPython.StartTime).TotalSeconds;exit_code=$actualPython.ExitCode;has_exited=$actualPython.HasExited;affinity=3}
    if(-not $actualPython.HasExited){$receipt.remaining_owned_pid=$actualPython.Id}
}
$receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $d ($Attempt+'-process.json')) -Encoding UTF8
$assertPath=Join-Path $d ('attempts/'+$Attempt+'/check-result.json')
$verdict=if($exitCode -eq 0 -and -not $forced -and $receipt.within_cap -and (Test-Path -LiteralPath $assertPath)){'BOUNDARY_PASS'}else{'BOUNDARY_FAIL_OR_INCOMPLETE'}
@{outcome=$verdict;exit_code=$exitCode;forced=$forced;assertion_file_present=(Test-Path -LiteralPath $assertPath)} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $d ($Attempt+'-verdict.json')) -Encoding UTF8
$receipt | ConvertTo-Json -Depth 6
Get-Content -LiteralPath (Join-Path $d ($Attempt+'-stdout.txt')) -Raw -Encoding UTF8
Get-Content -LiteralPath (Join-Path $d ($Attempt+'-stderr.txt')) -Raw -Encoding UTF8
