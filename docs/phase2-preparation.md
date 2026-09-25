# Phase-2 preparation: E041 candidate and E025 fallback

## Current A018 frozen delivery — 2026-09-25

This section supersedes the historical candidate choice and window-day commands
below. [A018](analysis/A018-test-selection.md) fixes comparison and selection:
**E041 selected**, E025 separately preserved, no TEST upload.

- Selected ZIP: `submissions/2026-09-25-E041.zip`, SHA256
  `bd5d2b7df3c39338f68cb08f125f85695073f37c9f4be3f6adcb8961941cd132`.
  Attach `submissions/2026-09-25-E041/method-4p.pdf` separately.
- Fallback ZIP: `submissions/2026-09-25-E025.zip`, SHA256
  `142921c3ea843c653821cf06a8b3fab89e8e6c96592581590f7e970064d90c6f`.
  Attach `submissions/2026-09-25-E025/method-4p.pdf` if fallback is chosen.
- Full [freeze manifest](analysis/A018-outputs/freeze-manifest.json) includes
  PDF hashes, executed check provenance and exact freeze UTC. Predictors retain
  original bytes; each new ZIP adds the complete starter-kit MIT notice only.
- E041 fresh final-ZIP official phase2 PASSx3, exact442425-vector source parity,
  official359.45s / inclusive364.34s. Single-process all3 E041336.55s,
  peak commitment1.60GB; E025332.78s/1.56GB. Local CPU limits and E025 historical
  official raw/provenance gap are documented; no hosted resource guarantee.
- Live official API rechecked2026-09-25: TEST Nov1 00:00UTC to **Nov14 00:00UTC
  (09:00KST)**, one submission/team; four-page method for every Test entry.
  Source license for non-commercial research reproduction required from top3
  at award stage. Scoped MIT proposal awaits owner choice; it is not a grant.
- Engineering change cutoff **Nov12 00:00UTC / 09:00KST**; preferred user upload
  by Nov13 00:00UTC. Any prior reopening needs new registered justification and
  full checks. After cutoff only organizer-required contract fixes with logs.
- Before user upload: recheck live rules and kit revision, verify manifest and
  chosen ZIP/PDF hashes, confirm the original authorized account and single
  unused TEST slot. New kit/schema invalidates affected certification and needs
  revalidation. No autonomous upload. E025 fallback is a pre-upload choice,
  never an assumed second attempt after a participant-side failure.

## Historical preparation records (preserved)

Update2026-09-24: E041 also completed local phase2 engineering qualification
(A012): official PASSx3, exact source/assembly vectors,367.177s inclusive local
time, paired UNHCR delta-.000508449 versus fresh E025, controls exact.
See [E041 comparison](../submissions/phase2-E041-preparation/SCORES.md).
The E041 four-page candidate method is now prepared and visually checked
(A013): `submissions/phase2-E041-preparation/method-4p-E041.pdf`, generated
from `docs/method-4p.md`. Final-model choice remains open. No hosted TEST upload.

The fallback remains `submissions/2026-09-09-E025/main.py`.
Preparation is local only; no new leaderboard or Test submission was made.
Its original method is preserved byte-for-byte at
`submissions/phase2-E025-preparation/method-4p-E025.pdf` and adjacent Markdown.
`output/pdf/method-4p.pdf` now describes E041. Pair any final archive with the
matching method; the historical E025 commands and audit below remain unchanged.

## Provenance and clock

This session continues the supplied 2026-09-21 handoff. The execution
environment reports 2026-09-18. Historical experiment outcomes through
September 21 are retained as supplied; the external checks below are a
September 18 snapshot and do not independently verify later history.

Baseline repository commit: `a6ea2173780b0b85efeec7f5f0829af055c63af0`.
E025 main.py SHA-256:

```
00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9
```

`git fetch origin` in `external/starter-kit` succeeded. Local HEAD and
origin/main both remain `ee427a9` (September 1, non-breaking description
wording); no pending gating update has shipped in this snapshot.

## Verified schedule and disclosure requirements

Sources: [competition and agreement](https://www.codabench.org/competitions/17822/),
[public API](https://www.codabench.org/api/competitions/17822/), and
[starter-kit license](https://github.com/SituatedEvals/public/blob/main/LICENSE).
The API's `terms` field was read directly; only terms and necessary schedule
fields were retained for this audit, not the full API response.

- Development ends at **2026-10-31 00:00 UTC**. Keep October 30 as the
  operational deadline.
- Test opens **2026-11-01 00:00 UTC / 09:00 KST** and ends
  **2026-11-14 00:00 UTC / 09:00 KST**. November 14 is not a full extra day.
  Plan upload by November 13 and recheck the live phase before uploading.
- Clause 7 requires a four-page method for every Test submission. The top
  three additionally provide source permitting non-commercial research
  reproduction at the award stage. Whole-repository public release is not
  expressly required. The website summary is less specific than this clause.
- Test has one submission per team and a 3,600-second shared budget.
  Clause 12 provides a retry for documented organizer infrastructure failure;
  do not assume a participant-side Test failure is retryable.
- External pretrained weights, if used, require a fixed commit before Test
  opens and suitable licensing (clause 9). E025 uses none. Public survey
  material informed hypotheses; no external training dataset or fitted prior
  enters the predictor.
- The kit is MIT-licensed. Preserve its notice when redistributing substantial
  kit-derived material. Dependency notices remain applicable. No new license
  is applied to our code by this preparation; select the team's release
  license before any award-stage delivery.

The September 2 within-dataset matching permission is an organizer-email
record in `docs/log.md`, not a new permission inferred from the API.
The historical E032 second-account reading remains disclosed in the method
and log; that account stays retired.

## Historical E025 method audit

- Corrected gate shrinkage: toward the median observed agreement, not one.
- Described held-out GIVEN frequencies used in matching without suggesting
  that held-out PREDICT answers enter training.
- Distinguished self-excluded replay from fully cross-fitted calibration;
  E025's replay base predictions are fitted on all visible rows.
- Removed assertions that hidden household structure was directly observed,
  all directional predictions transferred, or real-data optimality was proved.
- Synchronized sections 5 and 6 with unchanged phase-2 settings, the six
  flat A/Bs, E037's cross-fit loss, the probe map, and A005's synthetic ceiling.
- Preserved the historical 291-second runner measurement. It is distinct
  from the fresh 268.1-second source runner and 310.0-second official-scoring
  total, which includes driver overhead. Fresh source/assembly skill
  differences are exactly zero on all three instruments.

## Rebuild the attachment

Document-only dependencies used here: reportlab 5.0.1, pypdf 6.19.0,
PyMuPDF 1.28.2. They are not submission dependencies. They were installed
under `tmp/pdf-deps`, leaving the model environment unchanged.

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'tmp/pdf-deps')
.venv/Scripts/python.exe scripts/render_method.py
```

The renderer fails unless the result has exactly four pages. Render every
page to PNG with PyMuPDF (or Poppler) and inspect after document edits.
The continuation verified all four pages visually and checked text bounds.
The output PDF and ZIP paths are marked binary in `.gitattributes` to prevent
Windows newline conversion; staged artifact bytes were compared with disk.

## Window-day procedure

1. Recheck the live phase dates, agreement, and starter-kit remote. If the
   kit changed, inspect the diff and rerun the full local harness first.
2. Verify the original main.py SHA-256 above. Re-zip that file alone as
   root-level `main.py`; the PDF is a separate attachment, not model payload.
3. Run the archive checker. Confirm clean-sandbox no-regression against E025
   (absolute skill difference at most 0.002), source/assembly parity, and the
   official scorer on all three schemas with `--phase 2`. Preserve logs.
4. Copy `submissions/phase2-E025-preparation/SCORES.md` into the dated final
   snapshot before upload. Update verification hashes and times; retain the
   pre-registered interpretation arms. Re-render the method if facts changed.
5. Submit once through the original account and attach the four-page PDF.
   Record the submission identifier and exact Test scores. Test-vs-DEV
   differences are descriptive because the respondent roles differ.
6. Update the final SCORES.md, status, and top of log; commit and push origin.

Official rehearsal commands, from `external/starter-kit` (repeat for
`unicef`, `world_bank`, `unhcr`):

```powershell
../../.venv/Scripts/python.exe score.py --submission ../../submissions/2026-09-09-E025 --data _sandbox/unicef --schema data/unicef.json --phase 2
```

The CLI in `src/eval/runner.py` defaults to phase 1; for phase 2 call its
Python `run(predict_fn, schemas=[...], phase=2)` API. Do not label a default
CLI run as a phase-2 validation.

For source/assembly parity, run this Python from the repository root in the
model environment (sequentially, without competing training jobs):

```python
from src.eval.runner import load_predict, run
from src.models.hh_cap import predict

names = ["unicef", "world_bank", "unhcr"]
source = run(predict, schemas=names, phase=2)
assembled = run(load_predict("submissions/2026-09-09-E025/main.py"),
                schemas=names, phase=2)
for name in names:
    delta = source[name]["skill"] - assembled[name]["skill"]
    print(name, source[name]["skill"], assembled[name]["skill"], delta)
    assert abs(delta) <= 0.002
```

This continuation reused the fresh official scorer's assembly scores for
that comparison, rather than training the assembly a second time.

## Leaderboard snapshot

[Public leaderboard API](https://www.codabench.org/api/leaderboards/19827/)
shows six entries at UNHCR 0.93 / displayed Grand 0.65: in2ai, two SAPIENSQ
entries, mgjeon, tv, and AJK. This counts entries, not distinct teams.
AJK's entry is dated September 18. UNICEF is 0.52 throughout; World Bank is
0.49 or 0.50, so it is nearly constant rather than literally identical.
The next displayed plateau is Grand 0.64 / UNHCR 0.91-0.92.
This snapshot supplies no mechanism explaining our remaining gap and does
not change the phase-1 hold decision.
