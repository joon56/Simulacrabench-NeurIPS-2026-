param([ValidateRange(1,3)][int]$Cycle,[ValidateSet('reproduce','verify')][string]$Mode)
$ErrorActionPreference='Stop'
$root=(Get-Location).Path
$source=Join-Path $root 'docs/analysis/A040-outputs/modal-output-contract-repair1'
$temporary=Join-Path $root 'tmp/a040-modal-output-contract-repair1'
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-10-04T14:48:27Z')){throw 'Task deadline'}
$output=Join-Path $temporary "cycle$Cycle"
$snapshot=Join-Path $temporary "cycle$Cycle-source"
if((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $snapshot)){throw 'Cycle collision'}
$prior=@(Get-ChildItem -LiteralPath $temporary -Filter 'cycle*-process.json' -File | ForEach-Object {Get-Content -LiteralPath $_.FullName -Raw|ConvertFrom-Json})
if($prior.Count -ge 3){throw 'Cycle limit'}
$used=($prior|Measure-Object -Property elapsed_seconds -Sum).Sum
if($used -ge 120){throw 'Regression budget'}
New-Item -ItemType Directory -Path $snapshot | Out-Null
Get-ChildItem -LiteralPath $source -File | Where-Object {$_.Extension -eq '.py' -or $_.Name -eq 'source-manifest.json'} | Copy-Item -Destination $snapshot
$exe=Join-Path $root 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe'
$script=Join-Path $source 'tests_output_contract.py'
$stdout=Join-Path $temporary "cycle$Cycle-stdout.txt"
$stderr=Join-Path $temporary "cycle$Cycle-stderr.txt"
$watch=[Diagnostics.Stopwatch]::StartNew()
$process=Start-Process -FilePath $exe -ArgumentList @('-X','utf8','-B',('"'+$script+'"'),$Mode,('"'+$output+'"')) -PassThru -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr
$handle=$process.Handle
$timeout=-not $process.WaitForExit(40000)
if($timeout){Stop-Process -Id $process.Id -Force; $process.WaitForExit(5000)|Out-Null}
$watch.Stop()
$receipt=@{cycle=$Cycle;mode=$Mode;elapsed_seconds=$watch.Elapsed.TotalSeconds;exit_code=$process.ExitCode;timeout=$timeout;pid=$process.Id;remote_authorized=$false}
[IO.File]::WriteAllText((Join-Path $temporary "cycle$Cycle-process.json"),($receipt|ConvertTo-Json),[Text.UTF8Encoding]::new($false))
$receipt|ConvertTo-Json
Get-Content -LiteralPath $stdout -Encoding UTF8
Get-Content -LiteralPath $stderr -Encoding UTF8
