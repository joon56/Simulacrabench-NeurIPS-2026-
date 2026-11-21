$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) -Parent
$temp = Join-Path $root 'tmp/a040-modal-builder-source-repair1'
$python = Join-Path $root 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe'
$deadline = [DateTimeOffset]::Parse('2026-10-04T16:42:31Z')
if ([DateTimeOffset]::UtcNow.AddSeconds(115) -ge $deadline) { throw 'Insufficient task time' }
$cyclePath = Join-Path $PSScriptRoot 'cycle2-started.json'
if (Test-Path $cyclePath) { throw 'Cycle already started' }
@{cycle=2;started_utc=[DateTimeOffset]::UtcNow.ToString('o');scope='Local baseline then minimal change then fixed; no RPC'} | ConvertTo-Json | Set-Content -Encoding UTF8 $cyclePath
$watch = [Diagnostics.Stopwatch]::StartNew()
$records = @()
try {
  foreach ($mode in @('baseline','fixed')) {
    if ($mode -eq 'fixed') {
      # Only after actual SDK omission and missing isolated import are observed.
      $baseline = Get-Content -Encoding UTF8 (Join-Path $PSScriptRoot 'baseline-result.json') -Raw | ConvertFrom-Json
      if ($baseline.outcome -ne 'EXPECTED_SOURCE_CONTRACT_FAILURE_REPRODUCED') { throw 'No valid defect reproduction' }
      foreach ($name in @('sdk_endpoint.py','contract.py','live_launcher.py')) {
        $path = Join-Path $PSScriptRoot $name
        $bytes = [IO.File]::ReadAllBytes($path)
        $source = [Text.Encoding]::UTF8.GetString($bytes)
        if ($name -eq 'sdk_endpoint.py') {
          if (($source.Split(@('include_source=False'),[StringSplitOptions]::None)).Count -ne 2) { throw 'Unexpected flag occurrences' }
          $next = $source.Replace('include_source=False','include_source=True')
        } else {
          if (($source.Split(@('modal-output-contract-repair1'),[StringSplitOptions]::None)).Count -ne 2) { throw 'Unexpected placement occurrences' }
          $next = $source.Replace('modal-output-contract-repair1','modal-builder-source-repair1')
        }
        [IO.File]::WriteAllBytes($path,[Text.Encoding]::UTF8.GetBytes($next))
      }
    }
    $remaining = [Math]::Min(45,110-$watch.Elapsed.TotalSeconds)
    if ($remaining -lt 10) { throw 'Local check time exhausted' }
    $process = Start-Process -FilePath $python -ArgumentList @('-I','-B','-X','utf8', ('"'+$PSScriptRoot+'/check_builder_source.py"'),$mode) -WorkingDirectory $temp -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $PSScriptRoot ('cycle2-'+$mode+'-stdout.txt')) -RedirectStandardError (Join-Path $PSScriptRoot ('cycle2-'+$mode+'-stderr.txt'))
    $handle = $process.Handle
    if (!$process.WaitForExit([int]($remaining*1000))) {
      taskkill /PID $process.Id /T /F | Out-Null
      throw 'Owned check process timed out'
    }
    $process.WaitForExit()
    $records += @{mode=$mode;pid=$process.Id;exit_code=$process.ExitCode;elapsed_through_phase=$watch.Elapsed.TotalSeconds;hidden=$true}
    if ($process.ExitCode -ne 0) { throw ('Local phase failed: '+$mode) }
  }
} catch {
  $failure = $_.ToString()
} finally {
  @{cycle=2;outer_seconds=$watch.Elapsed.TotalSeconds;phases=$records;error=$failure;remote_authorized=$false} | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $PSScriptRoot 'cycle2.json')
}
if ($failure) { Write-Output $failure; exit 1 }
Write-Output 'Local baseline/fixed phases completed. Inspect result evidence before claiming PASS.'
