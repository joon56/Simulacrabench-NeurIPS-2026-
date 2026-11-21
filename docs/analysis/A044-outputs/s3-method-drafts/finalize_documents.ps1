$ErrorActionPreference = 'Stop'
$repoDir = (Get-Location).Path
$relativeOut = 'docs/analysis/A044-outputs/s3-method-drafts'
$outDir = Join-Path $repoDir $relativeOut
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Assert-Doc($condition, $message) { if (-not $condition) { throw $message } }
function Read-Json($name) { Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $outDir $name) | ConvertFrom-Json }
function Hash-File($path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower() }
function Hash-Text($value) {
    $digest = [System.Security.Cryptography.SHA256]::Create()
    try { ([System.BitConverter]::ToString($digest.ComputeHash($utf8NoBom.GetBytes($value)))).Replace('-', '').ToLower() }
    finally { $digest.Dispose() }
}
function Write-NewJson($name, $value) {
    $path = Join-Path $outDir $name
    Assert-Doc (-not (Test-Path -LiteralPath $path)) "Refuse existing $name"
    [System.IO.File]::WriteAllText($path, ($value | ConvertTo-Json -Depth 18), $utf8NoBom)
}

$entry = Read-Json 'entry.json'
$preservation = Read-Json 'preservation-entry.json'
$pairing = Read-Json 'document-pairing.json'
$ledger = Read-Json 'budget-ledger.json'
$visual = Read-Json 'visual-review.json'
$head = (& git -c safe.directory=C:/Users/USER/Desktop/SimulacraBench rev-parse HEAD).Trim()
Assert-Doc ($LASTEXITCODE -eq 0 -and $head -eq $entry.head) 'HEAD changed'
Assert-Doc ((Hash-File 'docs/workflow.md') -eq $entry.workflow_sha256) 'Workflow changed'
$priorRelease = Get-Content -Raw -Encoding UTF8 -LiteralPath docs/analysis/A044-outputs/s0-e025-review/verification.json | ConvertFrom-Json
Assert-Doc $priorRelease.exclusive_writer_released 'S0 release no longer present'
Assert-Doc ((Get-Date) -lt [DateTimeOffset]::Parse($entry.closeout_only_from).LocalDateTime) 'Past production threshold'

$preservationChecks = @()
foreach ($property in $preservation.PSObject.Properties) {
    if ($property.Name -in @('docs/status.md','docs/log.md','docs/phase2-preparation.md')) { continue }
    $actual = Hash-File $property.Name
    Assert-Doc ($actual -eq $property.Value) "Original changed: $($property.Name)"
    $preservationChecks += [ordered]@{path=$property.Name;sha256=$actual;matches_entry=$true}
}

$statusPath = Join-Path $repoDir 'docs/status.md'
$logPath = Join-Path $repoDir 'docs/log.md'
$phasePath = Join-Path $repoDir 'docs/phase2-preparation.md'
$currentStatus = [System.IO.File]::ReadAllText($statusPath)
$activeStart = $currentStatus.IndexOf('- **Active writer: S3-METHOD-DRAFTS-A044 /root, 2026-10-23.**')
$historyStart = $currentStatus.IndexOf('- **2026-10-23 S0 accepted E025 local phase2 provenance.**')
Assert-Doc ($activeStart -ge 0 -and $historyStart -gt $activeStart) 'Current writer notice changed'
$priorStatus = $currentStatus.Remove($activeStart, $historyStart-$activeStart)
$priorLog = [System.IO.File]::ReadAllText($logPath)
$priorPhase = [System.IO.File]::ReadAllText($phasePath)
Assert-Doc ((Hash-Text $priorStatus) -eq $preservation.'docs/status.md') 'Prior status bytes not preserved'
Assert-Doc ((Hash-Text $priorLog) -eq $preservation.'docs/log.md') 'Prior log changed concurrently'
Assert-Doc ((Hash-Text $priorPhase) -eq $preservation.'docs/phase2-preparation.md') 'Prior phase2 changed concurrently'

$pageChecks = @()
$requiredBanner = 'REVIEW DRAFT ' + [char]0x2014 + ' NOT FINAL TEST SELECTION'
foreach ($pair in $pairing.pairs) {
    Assert-Doc ((Hash-File $pair.main.path) -eq $pair.main.sha256) 'Main pairing mismatch'
    foreach ($document in $pair.documents) {
        Assert-Doc ((Hash-File $document.path) -eq $document.sha256) 'Document pairing mismatch'
    }
    $candidate = $pair.candidate
    Assert-Doc ((Hash-File "$outDir/$candidate-review.pdf") -eq (Hash-File "$outDir/$candidate-review-attempt1.pdf")) 'Final/attempt identity mismatch'
    $inspection = Read-Json "$candidate-pdf-inspection.json"
    Assert-Doc ($inspection.pages -eq 4 -and @($inspection.page_results).Count -eq 4) 'Actual page count'
    $uriCount = 0
    foreach ($page in $inspection.page_results) {
        Assert-Doc $page.text_bounds_pass 'Text bounds failed'
        Assert-Doc ($page.characters -gt 600) 'Near-empty page'
        $uriCount += @($page.links).Count
        Assert-Doc (Test-Path -LiteralPath "$outDir/$candidate-page-$($page.page).png") 'Page PNG missing'
    }
    Assert-Doc ($uriCount -eq 6) 'URI count'
    $firstPage = [System.IO.File]::ReadAllText("$outDir/$candidate-page-1.txt")
    Assert-Doc ($firstPage.Contains($requiredBanner)) 'Exact required draft banner missing'
    $pageChecks += [ordered]@{candidate=$candidate;actual_pages=4;uri_links=$uriCount;all_text_bounds=$true;all_four_pngs=$true;exact_banner=$true;final_matches_attempt1=$true}
}
Assert-Doc ($visual.result -eq 'PASS' -and @($visual.pages).Count -eq 8) 'Visual review incomplete'
$resources = @(Get-ChildItem -LiteralPath $outDir -Filter 'resource-*.json' | ForEach-Object {Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName | ConvertFrom-Json})
Assert-Doc ($resources.Count -eq 5) 'Unexpected document run count'
foreach ($record in $resources) {
    Assert-Doc ($record.passed -and $record.exit_code -eq 0 -and @($record.remnant_pids).Count -eq 0) 'Document run not closed'
}
$measured = ($resources | Measure-Object seconds -Sum).Sum
Assert-Doc ([Math]::Abs($measured - $ledger.measured_supervised_seconds) -lt 1e-9) 'Budget arithmetic'
Assert-Doc ($ledger.accounted_seconds -lt 300) 'Document budget'
Assert-Doc ($ledger.peak_sampled_tree_rss -lt 2147483648 -and $ledger.peak_sampled_tree_private -lt 2147483648) 'Memory budget'
$pythonProcesses = @(Get-Process -Name python,pythonw -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime)
Assert-Doc ($pythonProcesses.Count -eq 0) 'Python process still present; inspect before release'

$statusNotice = @'
- **2026-10-23 S3 method review drafts complete; writer released.**
  E041 and E025 each have an English4-page REVIEW DRAFT, with all8 pages inspected.
  E041 remains provisional/E025 alternative/E064 DEV waiting. No final choice,
  license grant or delivery approval. [S0 return](analysis/A044-outputs/s3-method-drafts/s0-handoff.ko.md),
  [verification/release](analysis/A044-outputs/s3-method-drafts/verification.json).
  New document budget charged125.5812167/300s, cash0; model/package/upload/commit/push0.
  S0 review pending; no active S3 writer after the linked release receipt.

### Earlier notices - historical; current S3 draft completion above

'@ + "`n"
$logNotice = @'
## 2026-10-23 - S3 completes E041/E025 review method drafts, returns to S0

- Current user approved S3-METHOD-DRAFTS-A044 and new gross60min/document300s/cash0.
  S0 release verified; S3 accepted sole writer17:28:46.0965403KST, workflow r6.
- Two English four-page PDFs plus Markdown; required REVIEW DRAFT banner.
  Actual page counts, text, fonts/formulas, margins and six URI links each passed;
  all eight PNG pages visually inspected. First PDF attempt succeeded for each.
- New E025442425 raw exact/official3 PASS is documented from completed records.
  No models reran; old drift/A012 provenance limits remain. E041 provisional,
  E025 alternative, E064 actual DEV result absent. Final TEST choice remains open.
- Current source/MD/PDF hashes paired with explicitly inherited ZIP identities.
  No ZIP access, notice change or license grant. Current Terms/exact Final times,
  rights holders, final model/account/slot/upload remain separate decisions.
- Five monitored document runs5.5812167s plus conservative120s overhead charge:
  125.5812167/300s; attempts2/6, cash0. Models/checker/package/network/upload/commit/push0.
- Original main/method/PDF/renderer identities and prior shared-document content
  preserved. All STOP/HOLD/exposure boundaries retained; writer released to S0
  review pending explicit acceptance. Exact time, dirty and process evidence:
  [verification](analysis/A044-outputs/s3-method-drafts/verification.json).
  [S0 handoff](analysis/A044-outputs/s3-method-drafts/s0-handoff.ko.md).

'@ + "`n"
$phaseNotice = @'
## Current S3 document completion - 2026-10-23

**REVIEW_DRAFTS_COMPLETE / FINAL_DELIVERY_NOT_APPROVED.**
New E041/E025 English review methods each passed actual4-page, text/link/bounds
checks and all8 PNG visual reviews. [S0 return](analysis/A044-outputs/s3-method-drafts/s0-handoff.ko.md),
[document hashes](analysis/A044-outputs/s3-method-drafts/document-pairing.json),
[open decisions](analysis/A044-outputs/s3-method-drafts/open-decisions.md).
No model/scorer/checker/ZIP work here. New E025 provenance is incorporated from
completed evidence; E041 was not rerun. E041 provisional/E025 alternative/E064
DEV waiting remain. Rights/license/current Terms/exact Final times/final choice/
account/slot/upload remain open. No TEST freeze, license grant or delivery approval.
S3 writer release and final jobs/budget are in the linked verification receipt.

### Earlier phase2 notices - retained historical planning

'@ + "`n"
$finalStatus = $priorStatus.Insert($activeStart, $statusNotice)
$logInsertAt = $priorLog.IndexOf("`r`n`r`n") + 4
$phaseInsertAt = $priorPhase.IndexOf("`r`n`r`n") + 4
Assert-Doc ($logInsertAt -ge 4 -and $phaseInsertAt -ge 4) 'Shared heading layout'
$finalLog = $priorLog.Insert($logInsertAt, $logNotice)
$finalPhase = $priorPhase.Insert($phaseInsertAt, $phaseNotice)
[System.IO.File]::WriteAllText($statusPath, $finalStatus, $utf8NoBom)
[System.IO.File]::WriteAllText($logPath, $finalLog, $utf8NoBom)
[System.IO.File]::WriteAllText($phasePath, $finalPhase, $utf8NoBom)
Assert-Doc ((Hash-Text ([System.IO.File]::ReadAllText($statusPath).Remove($activeStart,$statusNotice.Length))) -eq $preservation.'docs/status.md') 'Final status history'
Assert-Doc ((Hash-Text ([System.IO.File]::ReadAllText($logPath).Remove($logInsertAt,$logNotice.Length))) -eq $preservation.'docs/log.md') 'Final log history'
Assert-Doc ((Hash-Text ([System.IO.File]::ReadAllText($phasePath).Remove($phaseInsertAt,$phaseNotice.Length))) -eq $preservation.'docs/phase2-preparation.md') 'Final phase history'

# Establish inventory filenames before collecting the final dirty snapshot.
Write-NewJson 'verification.json' ([ordered]@{task=$entry.task;state='closeout in progress';exclusive_writer_released=$false})
[System.IO.File]::WriteAllText((Join-Path $outDir 'dirty-final.txt'), '', $utf8NoBom)
$dirty = @(& git -c safe.directory=C:/Users/USER/Desktop/SimulacraBench status --porcelain=v1 --untracked-files=all)
Assert-Doc ($LASTEXITCODE -eq 0) 'Git status failed'
$dirtyBefore = @([System.IO.File]::ReadAllLines((Join-Path $outDir 'dirty-entry.txt')))
$removed = @($dirtyBefore | Where-Object {$_ -notin $dirty})
$added = @($dirty | Where-Object {$_ -notin $dirtyBefore})
Assert-Doc ($removed.Count -eq 0) 'Prior dirty paths disappeared or changed status'
$unexpected = @($added | Where-Object {-not $_.StartsWith("?? $relativeOut/")})
Assert-Doc ($unexpected.Count -eq 0) 'Unexpected new dirty paths outside output folder'
[System.IO.File]::WriteAllText((Join-Path $outDir 'dirty-final.txt'), (($dirty -join "`n")+"`n"), $utf8NoBom)

$releaseAt = Get-Date
$grossSeconds = ($releaseAt - [DateTimeOffset]::Parse($entry.gross_start_conservative).LocalDateTime).TotalSeconds
Assert-Doc ($grossSeconds -lt 3600) 'Gross budget exceeded'
$artifactHashes = [ordered]@{}
foreach ($file in Get-ChildItem -LiteralPath $outDir -File | Sort-Object Name) {
    if ($file.Name -eq 'verification.json') { continue }
    $artifactHashes["$relativeOut/$($file.Name)"] = Hash-File $file.FullName
}
$sharedHashes = [ordered]@{}
foreach ($path in @('docs/status.md','docs/log.md','docs/phase2-preparation.md')) { $sharedHashes[$path] = Hash-File $path }
$verification = [ordered]@{
    task=$entry.task; verdict='REVIEW_DRAFTS_COMPLETE'; final_delivery='FINAL_DELIVERY_NOT_APPROVED';
    completed_at=$releaseAt.ToString('o'); head=$head; branch=$entry.branch;
    workflow_revision=$entry.workflow_revision; workflow_sha256=$entry.workflow_sha256;
    read_receipt='entry.json actual_read_order/read_evidence plus evidence-map.md and retained original PDF extraction';
    page_checks=$pageChecks; visual_pages_reviewed=8; pdf_attempts=$ledger.pdf_attempts;
    original_identity_checks=$preservationChecks; shared_prior_content_sha256=[ordered]@{status=$preservation.'docs/status.md';log=$preservation.'docs/log.md';phase2=$preservation.'docs/phase2-preparation.md'};
    shared_prior_content_preserved=$true; archive_open_or_rehash=$false;
    pairing_checked=$true; artifact_sha256=$artifactHashes; shared_document_sha256=$sharedHashes;
    dirty_entry_count=$dirtyBefore.Count; dirty_final_count=$dirty.Count; added_dirty_count=$added.Count;
    prior_dirty_paths_removed=$removed; unexpected_new_paths=$unexpected;
    preservation_limit='Enumerated original identities and prior shared text, plus dirty-path inventory; not a whole-tree rehash or all-chat attestation';
    gross_seconds=$grossSeconds; gross_limit_seconds=3600; measured_document_seconds=$measured;
    accounted_document_seconds=$ledger.accounted_seconds; document_limit_seconds=300;
    sampled_peak_tree_rss=$ledger.peak_sampled_tree_rss; sampled_peak_tree_private=$ledger.peak_sampled_tree_private;
    cpu_document_child=2; gpu=0; heavy=1; cash=0; credits=0;
    process_census_method='Get-Process python/pythonw plus five supervised owned-tree exit receipts; CIM denied, safer local fallback used';
    local_python_processes=$pythonProcesses; owned_jobs=@(); owned_descendants_remaining=@();
    model_runs=0; research_tests=0; checker_runs=0; packaging=0; network=0; installs=0; subagents=0;
    final_test_selection=$false; license_grant=$false; upload=0; commits=0; pushes=0;
    outgoing_writer='S3-METHOD-DRAFTS-A044 /root'; incoming_owner='S0 review pending explicit acceptance';
    exclusive_writer_released=$true; released_at=$releaseAt.ToString('o'); no_automatic_continuation=$true
}
[System.IO.File]::WriteAllText((Join-Path $outDir 'verification.json'), ($verification | ConvertTo-Json -Depth 18), $utf8NoBom)
[pscustomobject]@{verdict=$verification.verdict;release=$verification.released_at;gross_seconds=$grossSeconds;document_charged=$ledger.accounted_seconds;dirty_before=$dirtyBefore.Count;dirty_after=$dirty.Count;new_paths=$added.Count;owned_jobs=0;verification_sha256=(Hash-File (Join-Path $outDir 'verification.json'))} | ConvertTo-Json
